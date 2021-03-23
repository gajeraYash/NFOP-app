function countChar(val){
    var len = val.value.length;
    
    if (len >= 500) {
        val.value = val.value.substring(0, 499);
    } else if(len == 0){
        $('#char_count').text("");
    } else {
        $('#char_count').text(499 - len);
    }
}