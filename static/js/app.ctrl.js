YMApp.controller('YMCtrl', ['$scope', '$http', '$timeout', function($S, $H, $T) {
  
  $S.init = function() {
    
  };
  
  $S.submit = function(data) {
    if(!data || !data.nickname) return alert('닉네임을 입력해주세요.');
    if(!data.boardname) return alert('보드이름을 입력해주세요.');
    if(!data.bankname) return alert('입금자명을 입력해주세요.');
    if(!data.price || data.price < 1) return alert('입금 예상 금액을 입력해주세요.');
    if(!data.contact_number) return alert('연락처를 입력해주세요.');
    if(!data.idx && !data.password) return alert('비밀번호를 입력해주세요.');
    
    if(!confirm(data.idx?'본 내용으로 정보 수정을 진행하시겠습니까?':'본 내용대로 화환 참여를 진행하시겠습니까?')) return;
    $H.post('/process', data).success(function(res) {
      if(res.result > 0) return showError(res.result);
      alert(data.idx?'정보 수정이 완료되었습니다.':'등록이 완료되었습니다. 화환 프로젝트에 참여해주셔서 감사합니다!');
      document.location.reload();
    }).error(function() {
      alert('등록 중 오류가 발생했습니다. 번거로우시겠지만 문의를 부탁드립니다.');
    });
  };
  
  $S.cancel = function() {
    $S.data = {};
  };
  
  $S.edit = function() {
    $S.edata = {};
    $('#edit-popup').modal('show');
  };
  
  $S.submit2 = function(data) {
    if(!data || !data.nickname) return alert('닉네임을 입력해주세요.');
    if(!data.password) return alert('비밀번호를 입력해주세요.');
    
    $H.post('/check', data).success(function(res) {
      if(res.result > 0) return showError(res.result);
      $S.data = res.data;
      
      $S.edata = {};
      $('#edit-popup').modal('hide');
      
      $T(function() {
        $('html, body').animate({scrollTop: $('#join-form').offset().top}, 250);
      }, 100);
    }).error(function() {
      alert('정보 확인 중 오류가 발생했습니다. 번거로우시겠지만 문의를 부탁드립니다.');
    });
  };
  
  $S.remove = function(data) {
    if(!data.idx) return alert('신규 신청은 참가 철회를 할 수 없습니다.');
    if(!confirm('정말로 참가 신청을 철회하시겠습니까?')) return;
    $H.delete('/leave/' + data.idx).success(function(res) {
      if(res.result > 0) return showError(res.result);
      alert('참가 철회가 완료되었습니다. 가져주신 관심에 다시 한 번 감사드립니다.');
      document.location.reload();
    }).error(function() {
      alert('참가 철회 중 오류가 발생했습니다. 번거로우시겠지만 문의를 부탁드립니다.');
    });
  };
  
  $S.init();
}]);