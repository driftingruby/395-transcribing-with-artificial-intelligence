# pip install torch openai-whisper

import sys
import torch
import whisper
import warnings
from torch.multiprocessing import Process, Queue

warnings.filterwarnings("ignore")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = whisper.load_model("small.en").to(device)

def transcribe_audio(audio_file, output_queue):
  result = model.transcribe(audio_file)
  output_queue.put(result["text"])

def start_model_server(input_queue, output_queue):
  while True:
    audio_file = input_queue.get()
    if audio_file is None:
      break
    transcribe_audio(audio_file, output_queue)

if __name__ == "__main__":
  if torch.multiprocessing.get_start_method(allow_none=True) is None:
    torch.multiprocessing.set_start_method("spawn")

  input_queue = Queue()
  output_queue = Queue()
  model_process = Process(target=start_model_server, args=(input_queue, output_queue))
  model_process.start()

  while True:
    input_file = sys.stdin.readline().strip()
    if not input_file or input_file == "exit":
      input_queue.put(None)
      break
    input_queue.put(input_file)
    print(output_queue.get(), flush=True)
    print("___TRANSCRIPTION_END___", flush=True)
