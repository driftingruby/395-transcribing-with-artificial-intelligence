require "open3"

class Transcriber
  class NotAvailable < StandardError; end

  def initialize
    return unless ENV["WHISPER"] == 'true'
    @stdin, @stdout, @stderr, @wait_thr = Open3.popen3("python -u #{Rails.root.join("lib", "main.py")}")
  end

  def transcribe_audio(audio_file)
    raise Transcriber::NotAvailable unless @stdin
    @stdin.puts(audio_file)
    output = ""
    while line = @stdout.gets
      break if line.strip == "___TRANSCRIPTION_END___"
      output += line
    end
    output.strip
  rescue Errno::EPIPE
    @stdin, @stdout, @stderr, @wait_thr = Open3.popen3("python -u #{Rails.root.join("lib", "main.py")}")
    retry
  end
end

TRANSCRIBER = Transcriber.new