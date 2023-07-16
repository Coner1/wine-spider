kill -9 $(pgrep -f 'vivino_zh.py')

cd ~/wine-spider-combine-breed-area_breed_0
setsid python3 vivino_zh.py &>> out.log$(date "+%d_%H%M") 2>&1 &
cd ~/wine-spider-combine-breed-area_breed_100
setsid python3 vivino_zh.py &>> out.log$(date "+%d_%H%M") 2>&1 &
cd ~/wine-spider-combine-breed-area_breed_200
setsid python3 vivino_zh.py &>> out.log$(date "+%d_%H%M") 2>&1 &
cd ~/wine-spider-combine-breed-area_breed_300
setsid python3 vivino_zh.py &>> out.log$(date "+%d_%H%M") 2>&1 &
cd ~/wine-spider-combine-breed-area_breed_400
setsid python3 vivino_zh.py &>> out.log$(date "+%d_%H%M") 2>&1 &
cd ~/wine-spider-combine-breed-area_breed_500
setsid python3 vivino_zh.py &>> out.log$(date "+%d_%H%M") 2>&1 &
cd ~/wine-spider-combine-breed-area_breed_600
setsid python3 vivino_zh.py &>> out.log$(date "+%d_%H%M") 2>&1 &

ps aux| grep vivino_zh