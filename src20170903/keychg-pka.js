// javascript example for public-key authentication

function send_key(){
  var old_pubpem = localStorage["/~saka/pka4/ publicKey"];
  var old_prvpem = localStorage["/~saka/pka4/ privateKey"];
  var plain = new String(new Date());
  var oldpass = document.forms[0].oldpass.value;
  var old_pubkey = KEYUTIL.getKey(old_pubpem);
  var old_prvkey = KEYUTIL.getKey(old_prvpem, oldpass);
  var crypt = KJUR.crypto.Cipher.encrypt(plain, old_pubkey);
  if (plain != KJUR.crypto.Cipher.decrypt(crypt, old_prvkey)) {
    alert("Wrong old passphrase!");
    return false;
  }
  var pass = document.forms[0].newpass.value;
  if (pass != document.forms[0].vrfy.value) {
    alert("Two new passphrases are different!");
    return false;
  }
  document.forms[0].oldpass.value = "";
  document.forms[0].newpass.value = "";
  document.forms[0].vrfy.value = "";
  var keypair = KEYUTIL.generateKeypair("RSA", 2048);
  var prvkpem = KEYUTIL.getPEM(keypair.prvKeyObj, "PKCS5PRV", pass, "AES-256-CBC");
  localStorage["/~saka/pka4/ privateKey"] = prvkpem;
  var pubkpem = KEYUTIL.getPEM(keypair.pubKeyObj);
  localStorage["/~saka/pka4/ publicKey"] = pubkpem;
  document.forms[0].pubkey.value = pubkpem;
  return true;
}

// for save&load keys
var prvfile = document.getElementById('prvfile');
var pubfile = document.getElementById('pubfile');

function loadPrivate(e) {
  var fileData = e.target.files[0];
  var reader = new FileReader();
  reader.onload = function(e) {
    var data = reader.result;
    localStorage["/~saka/pka4/ privateKey"] = data;
  }
  reader.readAsText(fileData);
}
prvfile.addEventListener('change', loadPrivate, false);

function loadPublic(e) {
  var fileData = e.target.files[0];
  var reader = new FileReader();
  reader.onload = function(e) {
    var data = reader.result;
    localStorage["/~saka/pka4/ publicKey"] = data;
  }
  reader.readAsText(fileData);
}
pubfile.addEventListener('change', loadPublic, false);

function handlePrivate() {
  var content = localStorage["/~saka/pka4/ privateKey"];
  var blob = new Blob([ content ], { "type" : "text/plain" });
  if (window.navigator.msSaveBlob) { 
    window.navigator.msSaveBlob(blob, "privatekey.txt"); 
    window.navigator.msSaveOrOpenBlob(blob, "privatekey.txt"); 
  } else {
    document.getElementById("prvsave").href = window.URL.createObjectURL(blob);
  }
}

function handlePublic() {
  var content = localStorage["/~saka/pka4/ publicKey"];
  var blob = new Blob([ content ], { "type" : "text/plain" });
  if (window.navigator.msSaveBlob) { 
    window.navigator.msSaveBlob(blob, "publickey.txt"); 
    window.navigator.msSaveOrOpenBlob(blob, "publickey.txt"); 
  } else {
    document.getElementById("pubsave").href = window.URL.createObjectURL(blob);
  }
}

