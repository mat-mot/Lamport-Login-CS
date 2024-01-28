function hash(str) {
    const crypto = window.crypto || window.msCrypto;
    const buffer = new TextEncoder("utf-8").encode(str);
    let hash = crypto.subtle.digest("SHA-256", buffer)
    return hash.then(function (hash) {
        return hex(hash);
    });
}

function hex(buffer) {
    const hexCodes = [];
    const view = new DataView(buffer);
    for (let i = 0; i < view.byteLength; i += 4) {
        const value = view.getUint32(i)
        const stringValue = value.toString(16)
        const padding = '00000000'
        const paddedValue = (padding + stringValue).slice(-padding.length)
        hexCodes.push(paddedValue);
    }
    return hexCodes.join("");
}

function GetRepetitions(username) {
    let xhr = new XMLHttpRequest();
    let url = '/repetitions/';
    let data = {
      'username': username
    };
    let jsonData = JSON.stringify(data);
    xhr.open('POST', url, false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        return xhr.response
      }
      else
        console.log(4);
        return xhr.response
    };
    xhr.send(jsonData);
    return xhr.response
}

function hashPassword(password, repetitions) {
    return new Promise(function (resolve) {
        let hashedPassword = password;
        let count = 0;
        function hashNext() {
            if (count < repetitions - 1) {
                hash(hashedPassword).then(function (result) {
                    hashedPassword = result;
                    count++;
                    hashNext();
                });
            } else {
                resolve(hashedPassword);
            }
        }
        hashNext();
    });
}

$(document).ready(function () {
    $("#signin-form").submit(function (event) {
        event.preventDefault();
        const form = $(this);
        const username = form.find("input[name='username']").val();
        const password = form.find("input[name='password']").val();
        const repetitions = JSON.parse(GetRepetitions(username))['repetitions'];
        if (repetitions !== "Invalid request") {
        hashPassword(password, repetitions).then((hashedPassword) => {

        let xhr = new XMLHttpRequest();
        let url = form.attr('action');
        let method = form.attr('method').toUpperCase()
        let data = {
            'username': username,
            'password': hashedPassword,
            'repetitions': repetitions,
            'csrfmiddlewaretoken': form.find("input[name='csrfmiddlewaretoken']").val()
        };
        let jsonData = JSON.stringify(data);
        xhr.open(method, url, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function() {
          if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(3);
            document.getElementById('result').innerHTML = xhr.responseText
          }
          else
            console.log(4);
            document.getElementById('result').innerHTML = xhr.responseText
        };
        xhr.send(jsonData);

        }).catch(() => {
            console.log('password dosen\'t calculate')
        })
        }
        else {
            document.getElementById('error').innerHTML = 'Invalid Username or Password'
        }
    });
});
