import os, stat

# os.makedirs('all_music/test1')

main_path = 'main\\static\\all_music\\GlinoMess'
firt_track = os.path.join(main_path, os.listdir(main_path)[0])
os.chmod(firt_track, stat.S_IWRITE|stat.S_IREAD)
os.chmod(main_path, stat.S_IWRITE|stat.S_IREAD)
os.chmod('main\\static\\all_music\\KraboviySalat', stat.S_IWRITE|stat.S_IREAD)
os.symlink(firt_track, 'main\\static\\all_music\\KraboviySalat')
