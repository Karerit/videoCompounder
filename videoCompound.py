import moviepy.editor as mp
import pydub.silence
# from moviepy.editor import VideoFileClip, concatenate_videoclips
from pydub import AudioSegment
import os
import Compounder_UI

class video_dispose():
    def video_compound(self, sourcepath, localpath):
        try:
            self.namelist = os.listdir(sourcepath)

            files = [os.path.join(sourcepath + '\\' + video) for video in self.namelist]

            print(files)

            video_clips_list = self.extract_audio(files)

            # 创建视频剪辑列表
            video_clips = [mp.VideoFileClip(video) for video in video_clips_list]

            # 合成视频
            final_clip = mp.concatenate_videoclips(video_clips, method='compose')

            # 输出合成视频
            final_clip.to_videofile(localpath + '\\combined_video.mp4', fps=24)

        except Exception as e:
            print(e)

    # 分离音轨
    def extract_audio(self,files):
        clips = []
        for video in files:
            clip = mp.VideoFileClip(video)

            audio_file = 'extracted_audio.wav'
            # 提取音轨
            clip.audio.write_audiofile(audio_file)

            processed_audio_file = self.remove_background_noise(audio_file)

            clips.append(self.combine_audio_and_video(video, processed_audio_file))

        return clips

    #消除背景音
    def remove_background_noise(self,audio_file):
        sound = AudioSegment.from_file(audio_file)

        # 检测非静音区域
        nonsilence_ranges = pydub.silence.detect_silence(sound, min_silence_len=500, silence_thresh=sound.dBFS - 16)

        # 生成处理后音轨
        processed_audio = AudioSegment.silent(len(sound))

        for start, end in nonsilence_ranges:
            processed_audio += sound[start:end]

        processed_audio_file = 'processed_audio.wav'
        processed_audio.export(processed_audio_file, format='wav')

        return processed_audio_file

    # 将音频合回视频
    def combine_audio_and_video(self,video_file, audio_file):
        video = mp.VideoFileClip(video_file)
        audio = mp.AudioFileClip(audio_file)

        final_video = video.set_audio(audio)
        final_video_file = video_file[:-4] + '_work.mp4'
        final_video.write_videofile(final_video_file)
        return final_video_file

