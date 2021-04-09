from .tensorflow_infer import *


class RecordingThread(threading.Thread):
    def __init__(self, name, camera):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True

        self.cap = camera
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter('./static/video.avi', fourcc, 20.0, (640, 480))

    def run(self):
        while self.isRunning:
            ret, frame = self.cap.read()
            if ret:
                self.out.write(frame)

        self.out.release()

    def stop(self):
        self.isRunning = False

    def __del__(self):
        self.out.release()


class VideoCamera(object):
    def __init__(self):
        # self.rtmp_str = 'rtmp://58.200.131.2:1935/livetv/cctv1'
        self.rtmp_str = 'rtmp://120.55.55.230:1935/live/cs'
        # 打开摄像头， 0代表笔记本内置摄像头，或rtmp视频流路径
        self.cap = cv2.VideoCapture(self.rtmp_str)

        # # 初始化视频录制环境
        # self.is_record = False
        # self.out = None
        #
        # # 视频录制线程
        # self.recordingThread = None

    # 退出程序释放摄像头
    def __del__(self):
        self.cap.release()

    def get_frame(self):
        ret, frame = self.cap.read()

        if ret:
            ret, jpeg = cv2.imencode('.jpg', frame)

            # # 视频录制
            # if self.is_record:
            #     if self.out is None:
            #         fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            #         self.out = cv2.VideoWriter('./static/video.avi', fourcc, 20.0, (640, 480))
            #
            #     ret, frame = self.cap.read()
            #     if ret:
            #         self.out.write(frame)
            # else:
            #     if self.out is not None:
            #         self.out.release()
            #         self.out = None

            return jpeg.tobytes()

        else:
            return None

    def get_inferred_frame(self, output_video_name, conf_thresh):
        height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        # writer = cv2.VideoWriter(output_video_name, fourcc, int(fps), (int(width), int(height)))
        total_frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        if not self.cap.isOpened():
            raise ValueError("Video open failed.")
        status = True
        mask_record = 0
        no_mask_record = 0
        no_mask_warning = False
        while status:
            status, img_raw = self.cap.read()
            img_raw = cv2.cvtColor(img_raw, cv2.COLOR_BGR2RGB)
            if status:
                output_info = inference(img_raw,
                                        conf_thresh,
                                        iou_thresh=0.5,
                                        target_shape=(260, 260),
                                        draw_result=True,
                                        show_result=False)
                ret, jpeg = cv2.imencode('.jpg', img_raw[:, :, ::-1])
                # cv2.waitKey(1)
                mask = True
                for output in output_info:
                    if output[0] == 1:  # no mask
                        mask = False
                if not mask:
                    no_mask_record += 1
                    # 第一次检测到超过5帧未佩戴口罩，发出警告
                    if no_mask_record == 5:
                        mask_record = 0
                        no_mask_warning = True
                    # 5帧之后未佩戴口罩，清空警告标志
                    if no_mask_record != 5:
                        no_mask_warning = False
                else:
                    mask_record += 1
                    # 连续5帧内未发现未佩戴口罩情况，清空警告标志
                    if mask_record == 5:
                        no_mask_record = 0
                        no_mask_warning = False
                return jpeg.tobytes(), no_mask_warning

                # cv2.imshow('image', img_raw[:, :, ::-1])
                # writer.write(img_raw)
        return None

    # def start_record(self):
    #     self.is_record = True
    #     self.recordingThread = RecordingThread("Video Recording Thread", self.cap)
    #     self.recordingThread.start()
    #
    # def stop_record(self):
    #     self.is_record = False
    #
    #     if self.recordingThread is not None:
    #         self.recordingThread.stop()
