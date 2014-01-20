require 'mycroft'
require 'socket'

class Speakers < Mycroft::Client

  attr_accessor :verified

  def initialize
    @key = '/path/to/key'
    @cert = '/path/to/cert'
    @manifest = './app.json'
    @port = 3000
    @verified = false
  end

  def connect
    # Your code here
  end

  def on_data(data)
    puts data
    parsed = parse_message(data)
    if parsed[:type] == 'APP_MANIFEST_OK' or parsed[:type] == 'APP_MANIFEST_FAIL'
      check_manifest(parsed)
      @verified = true
      `ffplay rtp://127.0.0.1:#{@port}`
    elsif parsed[:type] == 'MSG_QUERY'
      #get ip address
      if parsed[:data]["action"] == "get ip"
        clientIP = Socket::getaddrinfo(Socket.gethostname,"echo",Socket::AF_INET)[0][3]
        content = {ip: clientIP, port: @port}
        query_success(parsed[:data]["id"], content)
      end
    end
  end

  def on_end
    # Your code here
  end
end

Mycroft.start(Speakers)
