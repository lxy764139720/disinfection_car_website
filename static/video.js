function play(scriptRoot) {
    var rtmp_address = '';
    $(function () {
        $.getJSON(scriptRoot + '/rtmp_address', {}, function (data) {
            rtmp_address = data.result;
            console.log(rtmp_address);
            if (flvjs.isSupported()) {
                var videoElement = document.getElementById('videoElement');
                var flvPlayer = flvjs.createPlayer({
                    type: 'flv',
                    url: rtmp_address
                });
                flvPlayer.attachMediaElement(videoElement);
                flvPlayer.load();
                flvPlayer.play();
            }
        });
        return false;
    });
}