#
# config.rb - Configure settings (& common subroutines)
#


# Common constants
USERNAME = "username"

# data dir
$data_dir = Dir.getwd + "/data/"

# session files
$sess_dir = $data_dir
$sess_prefix = "session-pka4."

# log file
$log_dir = $data_dir
$log_file = $log_dir + "pka4.log"

# DBs
$db_dir = $data_dir
$db_name = $db_dir + "db-pka4.db"

# URIs
$base_uri = "https://sakura.sakalab.org/~saka/pka4/"
$home_uri = $base_uri + "home.cgi"
$sign_out_uri = $base_uri + "signout.cgi"
# no authentication
#$sign_in_uri = $base_uri + "signin-0.cgi"
#$key_chg_uri = $base_uri + "NONE"
#$sign_up_uri = $base_uri + "NONE"
# password authentication
$sign_in_uri = $base_uri + "signin-pwd.cgi"
$key_chg_uri = $base_uri + "keychg-pwd.cgi"
$sign_up_uri = $base_uri + "signup-pwd.cgi"
# public-key authentication
$sign_in_uri = $base_uri + "signin-pka.cgi"
$key_chg_uri = $base_uri + "keychg-pka.cgi"
$sign_up_uri = $base_uri + "signup-pka.cgi"

# Emails
$from_email = "saka@slis.tsukuba.ac.jp"

# Common Subroutines
def esc_tags(s)
  r = s.gsub("&", "&amp;")
  r.gsub!(/"/, "&quot;")
  r.gsub!(/</, "&lt;")
  r.gsub!(/>/, "&gt;")
  return r
end

def plain2html(s)
  return s.gsub(/\R/, "<br/>\n")
end

def redirect_to(cgi, uri)
  cgi.out({
    "status" => "REDIRECT",
    "location" => uri
  }) {
    "redirect to ${uri}\n"
  }
end

