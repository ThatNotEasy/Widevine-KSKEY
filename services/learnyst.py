import base64, os
import glob
import hashlib
import json
import logging
import subprocess
import re
from enum import Enum
from os.path import splitext, basename, join
from queue import Queue
from urllib.parse import urlparse
import json
from os import makedirs
from os.path import exists, join
import requests
import wget
import xmltodict
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QObject, QEventLoop
from playwright._impl._errors import TargetClosedError
from playwright.sync_api import sync_playwright
from promise import promise
from pywidevine import PSSH, Device, Cdm
from modules.utils import handle, ensure_list, clean, try_parse, remove_query
from PyQt5.QtCore import QThread
from flask import Flask, request, send_file
from flask_cors import CORS

class NetworkFileManager(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        app = Flask(__name__)
        CORS(app)

        UPLOAD_FOLDER = 'files'
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

        @app.route('/upload', methods=['POST'])
        def upload_file():
            file_content = request.data

            file_path = os.path.join(UPLOAD_FOLDER, request.headers.get('Filename'))
            with open(file_path, 'wb') as file:
                file.write(file_content)

            return "OK", 200

        @app.route('/download/<filename>', methods=['GET'])
        def download_file(filename):
            file_path = os.path.join(UPLOAD_FOLDER, filename)

            if not os.path.exists(file_path):
                return "Not Found", 404

            return send_file(file_path, as_attachment=True)

        app.run(port=4444)
        
class PlayerManager:
    UNMODIFIED_PLAYER_NAME = "original_player.js"

    def __init__(
            self,
            token: str,
            version: int,
            lc: int,
            player_file: str
    ):
        self.token = token
        self.version = version
        self.lc = lc
        self.player_file = player_file

    def get_player(self) -> bool:
        b64_token = base64.b64encode(self.token.encode())

        sha256 = hashlib.new('sha256')
        sha256.update(b64_token)
        hashed = sha256.hexdigest()

        response = requests.get(
            url=f'https://player.learnyst.com/{hashed[:32]}/{hashed[32:]}/index.js',
            params={
                "tk": b64_token.decode(),
                "version": self.version,
                "lc": self.lc
            }
        )
        if response.status_code != 200:
            return False

        open(self.UNMODIFIED_PLAYER_NAME, "w", encoding="utf-8").write(response.text)
        return True

    @staticmethod
    def _find_and_insert(
            index_js: str,
            insert_index: int,
            rexp: str,
            name: str
    ) -> str:
        results = re.findall(rexp, index_js)

        handle(results, f"RegEx can't locate function: {rexp}")
        handle(len(results) == 1, f"RegEx found too many ({len(results)}) function results")

        return index_js[:insert_index] + f'exports.{name}={results[0]};' + index_js[insert_index:]

    @staticmethod
    def _find_insert_index(
            index_js: str,
            rexp: str
    ) -> int:
        found = re.findall(rexp, index_js)
        handle(found, f"regex can't locate function: {rexp}")
        handle(len(found) == 1, f"regex found too many ({len(found)}) function results")
        return index_js.index(found[0])

    @staticmethod
    def _find_and_insert_function(
            index_js: str,
            insert_index: int,
            rexp: str,
            name: str,
            function: str
    ) -> str:
        results = re.findall(rexp, index_js)
        handle(results, f"RegEx can't locate function: {rexp}")
        handle(len(results) == 1, f"RegEx found too many ({len(results)}) function results")
        return index_js[:insert_index] + f'exports.{name}={function % results[0]};' + index_js[insert_index:]

    def inject_exports(self):
        index_js = open(self.UNMODIFIED_PLAYER_NAME, "r", encoding="utf-8").read()
        SET_DRM_DATA_RE = r"let (_0x\w{3,6})={},_0x\w{3,6}=0,_0x\w{3,6}=0"
        SET_DRM_DATA_FUNCTION = r"function(value,key){%s[key]=value;}"
        # ENCRYPT_WITH_MD5_RE = r"function (_0x\w{3,6})\(_0x\w{3,6}\){var _0x\w{3,6}=_0x\w{3,6},_0x\w{3,6}=100,_0x\w{3,6}=_0x\w{3,6}"
        SET_CURRENT_LICENSE_RE = r"function (_0x\w{3,6})\(_0x\w{3,6},_0x\w{3,6},_0x\w{3,6},_0x\w{3,6},_0x\w{3,6}\){var _0x\w{3,6}=_0x\w{3,6};const _0x\w{3,6}=_0x\w{3,6}\(_0x\w{3,6},_0x\w{3,6},_0x\w{3,6},_0x\w{3,6},_0x\w{3,6}\);var _0x\w{3,6}={};return"
        ECRYPT_DECRYPT_BYTES_RE = r"(window\[_0x\w{3,6}\(\w+\)\])=function\(_0x\w{3,6},_0x\w{3,6},_0x\w{3,6}\)"
        ECRYPT_DECRYPTK_RE = r"function (_0x\w{3,6})\(_0x\w{3,6}\){var _0x\w{3,6}=_0x\w{3,6},_0x\w{3,6}=_0x\w{3,6}\[_0x\w{3,6}\(\w*\)\]\(_0x\w{3,6},_0x\w{3,6}\(\w*\)\)"
        INSERT_RE = r"exports\.getLicenseRequest=_0x\w{3,6};"
        index = self._find_insert_index(index_js, INSERT_RE)
        index_js = self._find_and_insert_function(index_js, index, SET_DRM_DATA_RE, "setDrmData", SET_DRM_DATA_FUNCTION)
        # index_js = self._find_and_insert(index_js, index, SET_DRM_DATA_RE, "setDrmData")
        # index_js = self._find_and_insert(index_js, index, ENCRYPT_WITH_MD5_RE, "encryptLicenseWithMd5Verifier")
        index_js = self._find_and_insert(index_js, index, SET_CURRENT_LICENSE_RE, "setCurrentLicense")
        index_js = self._find_and_insert(index_js, index, ECRYPT_DECRYPT_BYTES_RE, "ECRYPT_decrypt_bytes")
        index_js = self._find_and_insert(index_js, index, ECRYPT_DECRYPTK_RE, "ECRYPT_decryptk")
        open(self.player_file, "w", encoding="utf-8").write(index_js)
        return True

class ConfigManager:
    def __init__(self):
        self.config_dir_name = "cookies"
        self.config_file_name = join(self.config_dir_name, "config.json")
        self.defaults = {
            "lrToken": None
        }
        self.config = self.defaults

    def initialize(self):
        makedirs(self.config_dir_name, exist_ok=True)
        if not exists(self.config_file_name):
            js = json.dumps(self.config)
            with open(self.config_file_name, "w") as io_writer:
                io_writer.write(js)

    def read_config(self) -> bool:
        with open(self.config_file_name, "r") as io_reader:
            js = io_reader.read()
        try:
            jo = json.loads(js)
        except Exception as ex:
            print(f"Unable to parse json config file: {ex}")
            return False
        for key in self.config.keys():
            if key not in jo:
                print(f"Unable to locate key '{key}'in config file")
                continue
            self.config[key] = jo[key]

    def get(self, key: str):
        if key in self.config:
            return self.config[key]
        else:
            print(f"Key '{key}' is not a valid config key")

    def simple_get(self, key: str):
        self.read_config()
        return self.get(key)

    def write_config(self):
        js = json.dumps(self.config)
        with open(self.config_file_name, "w") as io_writer:
            io_writer.write(js)

    def set(self, key: str, value):
        if key in self.config:
            self.config[key] = value
        else:
            print(f"Key '{key}' is not a valid config key")

    def simple_set(self, key: str, value):
        self.set(key, value)
        self.write_config()
        
        
cM = ConfigManager()
cM.initialize()

class SrcType(Enum):
    UNENCRYPTED_IMAGE = 1
    ENCRYPTED_VIDEO = 2
    ENCRYPTED_PDF = 3
    UNENCRYPTED_VIDEO = 4
    YOUTUBE = 5
    VIMEO = 6
    TEST_TYPE = 7
    UNENCRYPTED_PDF = 8
    ZIP_CONTENT = 10
    ENCRYPTED_AUDIO = 12
    UNENCRYPTED_AUDIO = 13
    ENCRYPTED_IMAGE = 14
    ENCRYPTED_SCORM = 15
    UNENCRYPTED_SCORM = 16
    ENCRYPTED_TINCAN = 17
    UNENCRYPTED_TINCAN = 18
    ENCRYPTED_HTML = 19
    UNENCRYPTED_HTML = 20
    LIVE_LESSON = 21
    LEARNYST_LIVE_UNENCRYPTED = 22
    ATTACHMENT_TYPE = 50
    ATTACHMENT_TYPE_LINK = 51
    THUMBNAIL = 100


class DRMType(Enum):
    NO_DRM = 'ndrm'
    RESOURCES = 'resource'
    SDRM = 'sdrm'
    LDRM = 'ldrm'


class CommandEnum(Enum):
    ECRYPT_DECRYPTK = "ECRYPT_decryptk"
    ECRYPT_DECRYPT_BYTES = "ECRYPT_decrypt_bytes"
    SET_LICENSE = "setCurrentLicense"
    # ENCRYPT_WITH_MD5 = "encryptLicenseWithMd5Verifier"
    SET_DRM_DATA = "setDrmData"
    GET_LICENSE_REQUEST = "getLicenseRequest"  # predefined
    GET_URL_TOKEN = "getSignedUrlTok"  # predefined


class LearnystEnvironment(QThread):
    result_ready = pyqtSignal(str)

    def __init__(
            self,
            data_queue,
            library_path: str
    ):
        """
        Runs the learnyst javascript library in a headless Firefox browser
        Author: github.com/DevLARLEY
        """
        super().__init__()

        self.data_queue = data_queue
        self.running = True

        self.library = open(library_path, "r", encoding="utf-8").read()

    def run(self):
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            library_page = browser.new_page()

            library_page.goto("about:blank")
            library_page.on("console", lambda log: print(f'[LOG] {log}'))

            library_page.evaluate(self.library)
            self.wait_timeout(library_page)

    def wait_timeout(self, page):
        p = promise.Promise()

        while True:
            if not self.running:
                break

            if page.is_closed():
                logging.warning("Page has closed")

            if not self.data_queue.empty():
                if data_queue := self.data_queue.get():
                    if isinstance(data_queue, tuple):
                        returned = page.evaluate(*data_queue)
                    else:
                        returned = page.evaluate(data_queue)
                    self.result_ready.emit(returned)

            try:
                page.wait_for_timeout(1000)
            except TargetClosedError:
                logging.warning("Timeout failed")

        return p

    def stop(self):
        self.running = False


class LearnystInterface(QObject):
    def __init__(self):
        """
        Interface for interacting with the Learnyst Library Environment
        Author: github.com/DevLARLEY
        """
        super().__init__()

        self.data_queue = Queue()
        self.result = None

        self.worker_thread = LearnystEnvironment(
            data_queue=self.data_queue,
            library_path='player.js'
        )
        self.worker_thread.result_ready.connect(self.on_result_ready)
        self.worker_thread.start()

    def process_data(
            self,
            command: str | tuple
    ):
        self.data_queue.put(command)

        loop = QEventLoop()
        self.worker_thread.result_ready.connect(loop.quit)
        loop.exec_()

        return self.result

    def execute(
            self,
            command: CommandEnum,
            *args
    ):
        if command == CommandEnum.ECRYPT_DECRYPT_BYTES:
            return self.process_data(('''
                async (filename) => {
                    console.log("Receiving encrypted file...");
                    const response = await fetch('http://localhost:4444/download/' + filename);
                    const data = await response.arrayBuffer();
                    const bytes = new Uint8Array(data);

                    console.log("Decrypting...");
                    const result = LstPlayer.ECRYPT_decrypt_bytes(bytes, "%s", "%s");

                    console.log("Returning decrypted file...");
                    
                    const blob = new Blob([result], { type: 'application/octet-stream' });
                    await fetch('http://localhost:4444/upload', {
                        method: 'POST',
                        body: blob,
                        headers: {"Filename": filename}
                    });
                    return filename;
                }
                ''' % (args[1], args[2]), args[0]
            ))
        elif command == CommandEnum.SET_DRM_DATA:
            return self.process_data(
                "LstPlayer.{method}(JSON.parse('{arg0}'), '{arg1}')".format(
                    method=command.value,
                    arg0=json.dumps(args[0]),
                    arg1=args[1]
                )
            )
        elif command in (CommandEnum.GET_LICENSE_REQUEST, CommandEnum.SET_LICENSE):
            modified_args = map(
                lambda arg: '"{string}"'.format(string=arg),
                args
            )
            return self.process_data(
                'JSON.stringify(LstPlayer.{method}({args}))'.format(method=command.value, args=', '.join(modified_args))
            )
        else:
            modified_args = map(
                lambda arg: '"{string}"'.format(string=arg),
                args
            )
            return self.process_data(
                'LstPlayer.{method}({args})'.format(method=command.value, args=', '.join(modified_args))
            )

    @pyqtSlot(str)
    def on_result_ready(self, result):
        self.result = result

    def stop_processing(self):
        self.worker_thread.stop()
        self.worker_thread.wait()


class Learnyst:
    # ######## DO NOT TOUCH ######## #
    SHOULD_ENC_LIC = False  # not a requirement
    IS_PAID = True  # required in rare scenarios
    # ############################## #

    CDM_DIR = 'device'
    FILE_DIR = 'files'
    BIN_DIR = 'bin'

    def __init__(
            self,
            url: str,
            token: str
    ):
        """
        Learnyst Downloader
        Author: github.com/DevLARLEY
        """
        self.trash = []

        self.url = url
        self.token = token

        handle(
            devices := glob.glob(join(self.CDM_DIR, "*.wvd")),
            f"No widevine devices found in the {self.CDM_DIR!r} directory"
        )
        self.widevine_device = devices[0]

        self.network_manager = NetworkFileManager()
        self.network_manager.start()

        self.interface = LearnystInterface()
        self.title, self.sub_title, self.section_id, self.lesson_id = self._process_url(self.url)
        self.school_id, self.student_id, self.device_type = self._process_token(self.token)

    @staticmethod
    def _process_token(token: str) -> tuple[int, int, int]:
        split = token.split('.')[1]
        token_json = json.loads(base64.b64decode(split + '==').decode())
        return token_json.get('sid'), token_json.get('uid'), token_json.get('typ')

    @staticmethod
    def _process_url(url: str) -> tuple[str, str | None, int, int]:
        split = urlparse(url).path.split('/')
        return (
            split[split.index('home') + 1],
            course if (course := split[split.index('home') + 2]) not in ("section", "lesson") else None,
            int(split[split.index('section') + 1]),
            int(split[split.index('lesson') + 1])
        )

    @staticmethod
    def get_course_id(
            school_id: int,
            seo_title: str,
            token: str
    ) -> dict | None:
        response = requests.get(
            url=f'https://api.learnyst.com/learner/v17/courses/course_ids'
                f'?school_id={school_id}'
                f'&seo_title[]={seo_title}',
            headers={
                'Authorization': f'Bearer {token}'
            }
        )
        if "Course not found" in response.text:
            logging.error("Token likely doesn't match the site, delete config.json and try again")
        handle(response.status_code == 200, f"Unable to get course IDs ({response.status_code}): {response.text}")

        logging.debug(response.text)
        return response.json()

    def get_course_data(
            self,
            course_id: int,
            school_id: int,
            lesson_id: int,
            bundle_id: int = -1
    ) -> tuple | None:
        params = {'school_id': school_id}
        if bundle_id > 0:
            params.update({
                "bundle_id": bundle_id
            })

        response = requests.get(
            url=f'https://api.learnyst.com/learner/v17/courses/{course_id}',
            params=params,
            headers={
                'Authorization': f'Bearer {self.token}'
            }
        )
        handle(response.status_code == 200, f"Unable to get course data ({response.status_code}): {response.text}")
        logging.debug(response.text)
        course_data = response.json()

        if lessons := course_data.get('lessons'):
            if lesson_data := next(
                    (lesson.get('lesson_data') for lesson in lessons if lesson.get('id') == lesson_id),
                    None
            ):
                # TODO: ugly
                if not (course_data := json.loads(lesson_data)):
                    return
                data = course_data[0]
                return (
                    data.get('content_id', '').split('/')[0],
                    data.get('content_path'),
                    data.get('content_path_extn'),
                    data.get('duration'),
                    data.get('src'),
                    SrcType(data.get('src_type')),
                    course_id
                )
        elif bundles := course_data.get('bundle_courses'):
            if bundle := next(
                    (bundle for bundle in bundles if bundle.get('seo_title') == self.sub_title),
                    None
            ):
                return self.get_course_data(bundle.get('id'), school_id, lesson_id, course_id)

    @staticmethod
    def build_content_url(
            src_type: SrcType,
            content_path_extn: str,
            file_name: str
    ):
        if src_type == SrcType.LEARNYST_LIVE_UNENCRYPTED:
            # I won't support live streams (maybe on request)
            return
        e, d = content_path_extn.split('/')
        ext = splitext(file_name)[-1]
        match src_type:
            case SrcType.UNENCRYPTED_IMAGE:
                return f'{e}/ndrm/imgFile_uenc{ext}'
            case SrcType.ENCRYPTED_VIDEO | SrcType.ENCRYPTED_AUDIO:
                return f'{d}/sdrm/ctr/audio_video/stream.lds'
            case SrcType.ENCRYPTED_PDF:
                return f'{d}/ldrm/pdfFile_lenc.epdf'
            case SrcType.UNENCRYPTED_VIDEO | SrcType.UNENCRYPTED_AUDIO:
                return f'{e}/ndrm/audio_video/stream.mpd'
            case SrcType.UNENCRYPTED_PDF:
                return f'{e}/ndrm/pdfFile_uenc.pdf'
            case SrcType.ENCRYPTED_IMAGE:
                return f'{e}/ndrm/imgFile_uenc{ext}'
            case SrcType.UNENCRYPTED_HTML | SrcType.ENCRYPTED_HTML:
                return f'{e}/ndrm/sth/index.html'
            case _:
                handle(False, f"Unsupported src type ({src_type.name})")

    @staticmethod
    def get_drm_type(src_type: SrcType) -> DRMType:
        match src_type:
            case SrcType.ENCRYPTED_PDF:
                return DRMType.LDRM
            case SrcType.ENCRYPTED_VIDEO | SrcType.ENCRYPTED_AUDIO:
                return DRMType.SDRM
            case SrcType.YOUTUBE | SrcType.VIMEO:
                return DRMType.RESOURCES
            case _:
                return DRMType.NO_DRM

    def request_signed_url(
            self,
            token: str,
            content_path: str,
            drm_type: DRMType
    ) -> str | None:
        response = requests.post(
            url='https://api.learnyst.com/learner/v2/lessons/signed_url',
            headers={
                'Authorization': f'Bearer {self.token}',
            },
            json={
                'token': token,
                'content_folder': drm_type.value,
                'url_type': 1,  # static
                'content_path': content_path,
                'content_type': 1,  # static ('2' for questions)
                't': 0,  # TODO: isTrialUser
                'f': 1,  # TODO: isFreeCourse
                'p': 1,  # TODO: isPaidSchool
                'm': 1,  # TODO: isMonitorEnabled
            }
        )
        handle(response.status_code == 200, f"Unable to request signed URL ({response.status_code}): {response.text}")
        logging.debug(response.text)
        return response.json().get('signed_url')

    def generate_license_request(
            self,
            course_id: int,
            content_id: int,
            drm_type: DRMType
    ):
        logging.info("Getting license request...")
        handle(drm_type in (DRMType.SDRM, DRMType.LDRM), f"Can't generate request for DRMType {drm_type!r}")

        return self.interface.execute(
            CommandEnum.GET_LICENSE_REQUEST,
            self.school_id,
            self.student_id,
            course_id,
            self.lesson_id,
            -1, -1,  # both static
            content_id,
            self.SHOULD_ENC_LIC,
            self.IS_PAID,
            "invalid" if drm_type == DRMType.LDRM else "unknown",  # lstdrm: 'invalid', lgdrm: 'unknown' (??)
            lr_token,
            "web",  # static
            "NA" if drm_type == DRMType.LDRM else "cenc",  # lstdrm: 'NA', lgdrm: 'cenc'
            1,  # static
            "1",  # static
            drm_type == DRMType.LDRM  # lstdrm: True, lgdrm: False
        )

    def _decryption_setup(
            self,
            drm_type: DRMType,
            course_id: int,
            content_id: int,
            path_prefix: str
    ):
        license_request = self.generate_license_request(course_id, content_id, drm_type)
        license_request_json = json.loads(license_request)
        license_b64 = base64.b64encode(
            json.dumps({
                "licenseRequest": license_request_json.get('licRequest')
            }).encode()
        ).decode()

        logging.info("Requesting lst license...")
        lstdrm_request = requests.post(
            url='https://drm-u.learnyst.com/drmv2/lstdrm',
            headers={
                'x-lrtoken': lr_token,
                'x-lmul': '1',  # static
            },
            data=base64.b64encode(json.dumps({
                "appType": "web",  # static
                "browserName": "unknown",
                "browserOS": "unknown",
                "contentId": content_id,
                "contentPath": path_prefix,
                "courseId": course_id,
                "dbgStr": license_request_json.get('dbgStr'),
                "encAlgo": "aes" if self.SHOULD_ENC_LIC else "un",
                "isPaid": 1 if self.IS_PAID else 0,
                "lessonId": self.lesson_id,
                "licreq": license_b64,
                "md5": hashlib.md5(license_b64.encode('utf-8')).hexdigest(),
                "schoolId": self.school_id,
                "studentId": self.student_id,
                "ua": "unknown",
                "version": api_version
            }).encode()).decode()
        )

        if lstdrm_request.status_code == 412 and "This is not accessible for trail enrollment" in lstdrm_request.text:
            logging.info("Not accessible for trail enrollment, resending request")
            self.IS_PAID = False
            self._decryption_setup(drm_type, course_id, content_id, path_prefix)
            return

        handle(
            lstdrm_request.status_code == 200,
            f"Unable to request lst license ({lstdrm_request.status_code}): {lstdrm_request.text}"
        )
        logging.debug(lstdrm_request.text)

        logging.info("Decrypting lst license...")
        lst_license = self.interface.execute(CommandEnum.ECRYPT_DECRYPTK, lstdrm_request.text)
        handle(json_license := try_parse(lst_license), "Unable parse lst license, report this on GitHub")

        logging.info("Setting lst license...")
        set_license = self.interface.execute(
            CommandEnum.SET_LICENSE,
            self.school_id,
            self.student_id,
            self.lesson_id,
            json_license.get('lstLicense'),
            path_prefix
        )
        handle(set_license_json := try_parse(set_license), f"Unable to parse SET_LICENSE result: {set_license}")
        if (result := set_license_json.get('result')) != 1000000:
            logging.warning(f"SET_LICENSE result does not indicate success ({result})")

        logging.info("Setting drm data...")
        self.interface.execute(
            CommandEnum.SET_DRM_DATA,
            {
                "schoolId": self.school_id,
                "studentId": self.student_id,
            },
            path_prefix
        )

    def _get_file(
            self,
            src_type: SrcType,
            drm_type: DRMType,
            course_id: int,
            content_id: int,
            path_prefix: str,
            path_prefix_extn: str,
            src: str
    ):
        logging.info("Getting signed URL...")
        url_token = self.interface.execute(
            CommandEnum.GET_URL_TOKEN,
            self.school_id,
            self.student_id,
            course_id,
            self.lesson_id
        )
        signed_url = self.request_signed_url(url_token, path_prefix, drm_type)

        if drm_type != DRMType.NO_DRM:
            self._decryption_setup(drm_type, course_id, content_id, path_prefix)

        content_path = self.build_content_url(src_type, path_prefix_extn, src)
        source_file_url = signed_url.replace('*', content_path)

        if src_type in (
                SrcType.UNENCRYPTED_HTML, SrcType.UNENCRYPTED_IMAGE, SrcType.UNENCRYPTED_PDF,
                SrcType.UNENCRYPTED_VIDEO, SrcType.UNENCRYPTED_AUDIO, SrcType.ENCRYPTED_HTML
        ):
            source_file_url = remove_query(source_file_url)

        file_request = requests.get(source_file_url)
        handle(
            file_request.status_code == 200,
            f"Unable to request resource file ({file_request.status_code}): {file_request.text}"
        )

        content = file_request.content

        # manifest
        if src_type in (
                SrcType.ENCRYPTED_VIDEO, SrcType.ENCRYPTED_AUDIO, SrcType.UNENCRYPTED_VIDEO, SrcType.UNENCRYPTED_AUDIO
        ):
            src = basename(content_path)
            self.trash.append(join(self.FILE_DIR, src))

        open(join(self.FILE_DIR, src), "wb").write(content)

        if drm_type != DRMType.NO_DRM:
            logging.info("Decrypting file...")
            src = join(self.FILE_DIR, self.interface.execute(CommandEnum.ECRYPT_DECRYPT_BYTES, src, 0, source_file_url))
        else:
            src = join(self.FILE_DIR, src)
            logging.info(f"Unencrypted file URL => {source_file_url}")

        return src, source_file_url

    def _download_manifest(
            self,
            manifest: str,
            url: str,
            decrypt: bool
    ) -> tuple[list[str], str]:
        with open(manifest, "r") as io_reader:
            manifest_json = xmltodict.parse(io_reader.read())
        self.trash.append(manifest)

        files = []
        pssh = None
        for ad_set in ensure_list(manifest_json["MPD"]["Period"]["AdaptationSet"]):
            if ad_set["@contentType"] in ("video", "audio"):
                if decrypt:
                    pssh = next(
                        protection.get('cenc:pssh') for protection in ensure_list(ad_set["ContentProtection"])
                        if protection.get('@schemeIdUri').lower() == "urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed"
                    )
                representation = sorted(
                    ensure_list(ad_set.get('Representation')), key=lambda i: int(i.get('@bandwidth')), reverse=True
                )

                name = representation[0].get('BaseURL')
                logging.info(f'Downloading {name}...')
                manifest_name = "stream.lds" if decrypt else "stream.mpd"
                files.append((
                    wget.download(
                        url=(modified := url.replace(manifest_name, name)),
                        out=join(self.FILE_DIR, name)
                    ),
                    modified
                ))
                print()
        if decrypt:
            for idx, (file, furl) in enumerate(files):
                logging.info(f'Decrypting {file} (this can take a while)...')
                self.trash.append(file)
                decrypted_file = self.interface.execute(
                    CommandEnum.ECRYPT_DECRYPT_BYTES,
                    basename(file),
                    0,
                    furl
                )
                files[idx] = (join(self.FILE_DIR, decrypted_file), furl)
        return list(map(
            lambda f: f[0],
            files
        )), pssh

    def _get_keys(
            self,
            course_id: int,
            content_id: int,
            drm_type: DRMType,
            path_prefix: str,
            pssh: str,
            widevine_device: str
    ) -> list[str]:
        device = Device.load(widevine_device)
        cdm = Cdm.from_device(device)
        session_id = cdm.open()
        challenge = cdm.get_license_challenge(session_id, PSSH(pssh))
        challenge += b'\xaa\xa0\x20\x10\x00\x00\x01\x00\x00\x00'  # static

        license_request = self.generate_license_request(course_id, content_id, drm_type)
        license_request_json = json.loads(license_request)
        license_b64 = base64.b64encode(
            json.dumps({
                "licenseRequest": license_request_json.get('licRequest'),
                "rawLicenseRequest": base64.b64encode(challenge).decode()
            }).encode()
        ).decode()

        logging.info("Requesting lgdrm license...")
        lgdrm_request = requests.post(
            url='https://drm-u.learnyst.com/drmv2/lgdrm',
            headers={
                'x-lrtoken': lr_token,
                'x-lmul': '1',  # static
            },
            data=base64.b64encode(json.dumps({
                "appType": "web",  # static
                "browserName": "unknown",
                "browserOS": "unknown",
                "contentId": content_id,
                "contentPath": path_prefix,
                "courseId": course_id,
                "dbgStr": license_request_json.get('dbgStr'),
                "encAlgo": "aes" if self.SHOULD_ENC_LIC else "un",
                "isPaid": 1 if self.IS_PAID else 0,
                "lessonId": self.lesson_id,
                "licreq": license_b64,
                "md5": hashlib.md5(license_b64.encode('utf-8')).hexdigest(),
                "schoolId": self.school_id,
                "studentId": self.student_id,
                "ua": "unknown",
                "version": api_version
            }).encode()).decode()
        )
        handle(
            lgdrm_request.status_code == 200,
            f"Unable to request widevine license ({lgdrm_request.status_code}): {lgdrm_request.text}"
        )
        logging.debug(lgdrm_request.text)

        logging.info("Decrypting lgdrm license...")
        lgdrm_license = self.interface.execute(CommandEnum.ECRYPT_DECRYPTK, lgdrm_request.text)
        handle(
            json_license := try_parse(lgdrm_license),
            "Unable parse widevine license, report this on GitHub"
        )

        raw_license_response = json_license.get('rawLicenseResponse')
        cdm.parse_license(session_id, raw_license_response)

        keys = list(map(
            lambda key: f"{key.kid.hex}:{key.key.hex()}",
            filter(
                lambda key: key.type == 'CONTENT',
                cdm.get_keys(session_id)
            )
        ))

        cdm.close(session_id)
        return keys

    def _decrypt(
            self,
            files: list,
            keys: list
    ):
        for file in files:
            split = list(splitext(file))
            split.insert(1, ".dec")
            new_name = ''.join(split)

            command = []
            if executable_exists("shaka-packager"):
                logging.info("Decrypting using Shaka Packager...")
                command = [
                    join(self.BIN_DIR, "shaka-packager"),
                    "--minloglevel=2",
                    f"input={file},stream={'audio' if basename(file).startswith('a') else 'video'},output={new_name}",
                    "--enable_raw_key_decryption",
                    *sum([['--keys', i] for i in map(lambda key: 'key_id=' + key[:33] + 'key=' + key[33:], keys)], [])
                ]
            elif executable_exists("mp4decrypt"):
                logging.info("Decrypting using mp4decrypt...")
                command = [
                    join(self.BIN_DIR, "mp4decrypt"),
                    file,
                    new_name,
                    *sum([['--key', i] for i in keys], [])
                ]

            handle(command, "Unable to locate neither shaka-packager nor mp4decrypt")
            subprocess.run(command, shell=False)
            yield new_name

    def _merge(
            self,
            files: list,
            name: str
    ):
        command = []
        new = join(self.FILE_DIR, splitext(name)[0] + ".mkv")

        if executable_exists("ffmpeg"):
            logging.info("Muxing using ffmpeg...")
            command = [
                join(self.BIN_DIR, "ffmpeg"), "-y",
                "-loglevel", "error",
                *sum([['-i', i] for i in files], []),
                "-c", "copy",
                new
            ]
        elif executable_exists("mkvmerge"):
            logging.info("Muxing using mkvmerge...")
            command = [
                join(self.BIN_DIR, "mkvmerge"),
                "-q",
                *files,
                "-o", new
            ]

        handle(command, "Unable to locate neither ffmpeg nor mkvmerge")
        subprocess.run(command, shell=False)
        # noinspection PyUnboundLocalVariable
        return new

    def download(self):
        logging.info("Requesting course id...")
        # TODO: select from output
        course = self.get_course_id(self.school_id, self.title, self.token)
        logging.debug(course)
        course_id = course[0].get('id')

        logging.info("Requesting course data...")

        handle(data := self.get_course_data(course_id, self.school_id, self.lesson_id), "Unable to get course data")
        content_id, path_prefix, path_prefix_extn, duration, src, src_type, bundle_course_id = data

        logging.info(f"Content Type => {src_type.name}")

        if src_type == SrcType.TEST_TYPE:
            handle(False, "Content type is not supported")

        if self.sub_title:
            course_id = bundle_course_id
        drm_type = self.get_drm_type(src_type)

        match src_type:
            case SrcType.ENCRYPTED_PDF:
                file = self._get_file(src_type, drm_type, course_id, content_id, path_prefix, path_prefix_extn, src)
                logging.info(f"Decrypted PDF => {file[0]}")

            case SrcType.ENCRYPTED_VIDEO | SrcType.ENCRYPTED_AUDIO:
                mpd, url = self._get_file(src_type, drm_type, course_id, content_id, path_prefix, path_prefix_extn, src)
                files, pssh = self._download_manifest(mpd, url, True)
                self.trash.extend(files)

                keys = self._get_keys(course_id, content_id, drm_type, path_prefix, pssh, self.widevine_device)
                decrypted = list(self._decrypt(files, keys))
                self.trash.extend(decrypted)

                merged = self._merge(decrypted, src)
                logging.info(f"Decrypted Video/Audio => {merged}")

            case SrcType.UNENCRYPTED_VIDEO | SrcType.UNENCRYPTED_AUDIO:
                mpd, url = self._get_file(src_type, drm_type, course_id, content_id, path_prefix, path_prefix_extn, src)
                files, pssh = self._download_manifest(mpd, url, False)
                self.trash.extend(files)

                merged = self._merge(files, src)
                logging.info(f"Unencrypted Video/Audio => {merged}")

            case SrcType.YOUTUBE | SrcType.VIMEO:
                logging.info(f"Resource => {src}")

            case _:
                file = self._get_file(src_type, drm_type, course_id, content_id, path_prefix, path_prefix_extn, src)
                logging.info(f"Unencrypted File => {file[0]}")

        clean(self.trash)

        self.interface.stop_processing()