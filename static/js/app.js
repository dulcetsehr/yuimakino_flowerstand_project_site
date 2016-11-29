var showError = function(code) {
  if(code == 1) alert('닉네임을 입력해주세요.');
  if(code == 2) alert('보드이름을 입력해주세요.');
  if(code == 3) alert('입금자명을 입력해주세요.');
  if(code == 4) alert('입금 예상 금액을 입력해주세요.');
  if(code == 5) alert('연락처를 입력해주세요.');
  if(code == 6) alert('비밀번호를 입력해주세요.');
  if(code == 7) alert('수정 권한이 없습니다.');
  if(code == 8) alert('해당 닉네임 및 비밀번호로 등록된 정보가 없습니다. 닉네임 및 비밀번호를 다시 한 번 확인 후 입력해주세요.');
};



var YMApp = angular.module('YMApp', ['YMCtrls', 'YMFilters']);
var YMCtrls = angular.module('YMCtrls', []);

angular.module('YMFilters', [])
.filter('nl2br', function() {
  return function(text) {
    return text ? text.replace(/\n/g, '<br>') : text;
  };
})
.filter('striptags', function() {
  return function(text) {
    try {
      return angular.element(text).text();
    } catch(e) {
      return text;
    }
  };
})
.filter('autolink', function() {
  return function linkify(inputText) {
    if(!inputText) return;
    var replacedText, replacePattern1, replacePattern2, replacePattern3;
    replacePattern1 = /(\b(https?|ftp):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/gim;
    replacedText = inputText.replace(replacePattern1, '<a href="$1" target="_blank">$1</a>');
    replacePattern2 = /(^|[^\/])(www\.[\S]+(\b|$))/gim;
    replacedText = replacedText.replace(replacePattern2, '$1<a href="http://$2" target="_blank">$2</a>');
    replacePattern3 = /(([a-zA-Z0-9\-\_\.])+@[a-zA-Z\_]+?(\.[a-zA-Z]{2,6})+)/gim;
    replacedText = replacedText.replace(replacePattern3, '<a href="mailto:$1">$1</a>');
    return replacedText;
  };
})
.filter('escape', function() {
  return function(s) {
    return s ? s.replace(/[&"'<>]/g,function(m){return"&"+["amp","quot","#039","lt","gt"]["&\"'<>".indexOf(m)]+";"}) : s;
  };
})
.filter('range', function() {
  return function(input, start, end, step) {
    start = start >> 0;
    end = end >> 0;
    step = step >> 0;
    if(step <= 0) step = 1;
    
    var direction = (start <= end) ? step : -step;
    while (start != end) {
        input.push(start);
        start += direction;
    }
    return input;
  };
})
;




