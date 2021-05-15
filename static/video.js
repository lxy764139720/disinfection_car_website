function play(scriptRoot) {
    var rtmp_address = '';
    $(function () {
        $.getJSON($SCRIPT_ROOT + '/rtmp_address', {}, function (data) {
            rtmp_address = data.result;
            console.log('inner');
            console.log(rtmp_address);
            if (flvjs.isSupported()) {
                var videoElement = document.getElementById('videoElement');
                console.log('outer');
                console.log(rtmp_address);
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