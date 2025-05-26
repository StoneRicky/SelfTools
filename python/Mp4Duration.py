from moviepy.editor import VideoFileClip
 
video_path = 'C:\\Users\\Medcare\\Downloads\\WeChat_20240913093025.mp4'  # 替换为你的视频文件路径
video_clip = VideoFileClip(video_path)
print(video_clip.duration)