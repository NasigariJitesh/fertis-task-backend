

echo "Starting server..."
tmux new-session -d -s server
tmux send-keys -t server "source venv/bin/activate" C-m
tmux send-keys -t server "export ENVIRONMENT=development" C-m
tmux send-keys -t server "python3 main.py" C-m
tmux send-keys -t server "uvicorn server.main:app --reload --host 0.0.0.0 --port 4000" C-m
echo "Started server"

echo "All sessions started successfully!"
