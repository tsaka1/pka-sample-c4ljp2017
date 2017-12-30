#!/usr/local/bin/ruby
#
# An example of sign-up for public-key authentication
#

require("cgi")
require("cgi/session")
require("logger")
require("sqlite3")
require("digest/sha1")
require("securerandom")
require("net/smtp")

load(Dir.getwd + "/config.rb")

log = Logger.new($log_file)
log.level = Logger::INFO

cgi = CGI.new
sess = CGI::Session.new(cgi, {
  "session_secure" => true,
  "tmpdir" => $sess_dir,
  "prefix" => $sess_prefix
  })

u_name = cgi["email"]
u_pass = cgi["kwd"]
salt = nil
pass = nil
stat = nil
db = SQLite3::Database.new($db_name)
begin
  if u_name !~ /^[^@]+@[^@]+$/ || u_pass !~ /^sakaguchi/i
    redirect_to(cgi, $sign_in_uri)
    log.info($0) { "invalid email or keyword, redirect to #{$sign_in_uri}" }
  else
    salt = SecureRandom.hex(10)
    u_pass = SecureRandom.hex(10)
    pass = Digest::SHA1.hexdigest(salt + u_pass)
    stat = "reset"
    begin
      db.transaction{
	db.execute("delete from pka where email = ?;", u_name)
	db.execute("insert into pka (email, salt, pubkey, status) \
	  values (?, ?, ?, ?);", u_name, salt, pass, stat)
      }
    rescue SQLite3::BusyException
      sleep(0.1)
      retry
    end
    Net::SMTP.start('localhost', 25) {|smtp|
      smtp.send_message(<<-"EOM", $from_email, u_name)
From: #{$from_email}
To: #{u_name}
Subject: pka4 - PIN for Sign-up / Keypair reset

Your PIN is: #{u_pass}
--
admin of #{$home_uri}
      EOM
    }
    cgi.out(
      "status" => "OK",
      "type" => "text/html",
      "charset" => "utf-8"
    ){
      <<-"EOS"
      <html>
      <head>
      <title>Sign-Up / Keypair reset, 2nd step.</title>
      </head>
      <body>
      <h1>Sign-Up / Keypair reset, 2nd step.</h1>
      <form method="POST" action="signup-pka2.cgi">
	Email: <input name="email" type="text" size="40" /><br/>
	PIN: <input name="pin" type="password" size="20" /><br/>
	<input type="submit" />
	<input type="reset" />
      </form>
      <hr/>
      </body>
      </html>
      EOS
    }
  end
  log.info($0) { "sent PIN via email and respond 2nd step form." }
ensure
  db.close
end

log.close
