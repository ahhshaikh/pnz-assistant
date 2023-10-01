const url = require('url');

export function getUrlQueryParams(uri) {
  const url_parts = url.parse(uri, true);
  return Object.assign({}, getHashParams(url_parts.hash.slice(1)), url_parts.query);
}
function getHashParams(q) {
  var hashParams = {};
  var e;
  var a = /\+/g;  // Regex for replacing addition symbol with a space
  var r = /([^&;=]+)=?([^&;]*)/g;
  var d = function (s) { return decodeURIComponent(s.replace(a, " ")); };
  while (e = r.exec(q))
    hashParams[d(e[1])] = d(e[2]);
  return hashParams;
}

