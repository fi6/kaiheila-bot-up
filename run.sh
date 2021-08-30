NOW=$(date +"%H-%M-%S")
DATE=$(date +"%m-%d-%y")
mkdir -p logs/$DATE
export PROJECT_DIR=/home/fi/tools/kaiheila-bot-up
PID=$(cat run.pid)
PID_EXIST=$(ps aux | awk '{print $2}'| grep -w $PID)
if ps -p $PID > /dev/null
then
   echo "$PID is running"
   kill $PID
   echo "$PID killed"
   # Do something knowing the pid exists, i.e. the process with $PID is running
fi
source "$PROJECT_DIR"/.venv/bin/activate
nohup python "$PROJECT_DIR"/app.py &> "$PROJECT_DIR"/logs/$DATE/$NOW.log & echo $! > run.pid
echo "run at pid $(cat run.pid)"
unset -v latest
sleep 1
for file in "$PROJECT_DIR"/logs/*/*; do
  [[ $file -nt $latest ]] && latest=$file
done
tail -vf -n 30 $file