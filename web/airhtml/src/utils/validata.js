/**
 * 验证邮箱:let reg = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/
 * 字母+数字:let reg = /^(?!\D+$)(?![^a-zA-Z]+$)\S{6,20}$/
 * 字母或数字:let reg = /^[a-zA-Z]{6}|[0-9]{6}$/
 * 过滤特殊字符
 * export:将接口暴露出去
 */
export function stripscript(str) {
	/*
	完整过滤：
	"[`~!@#$^&*()=|{}':;',\\[\\].<>/?~！@#￥……&*（）——|{ }【】‘；：”“'。，、？]"
	一般密码特殊字符：
	$@%#
	*/
	var pattern = new RegExp("[`~!^&*()=|{}':;',\\[\\].<>/?！￥……&*（）——|{ }【】‘；：”“'。，、？]")
	var rs = "";
	for (var i = 0; i < str.length; i++) {
		rs = rs + str.substr(i, 1).replace(pattern, '');
	}
	return rs;
}

/**
 * 验证邮箱
 */
export function validatamailbox(value){
	let reg = /^(([a-zA-Z]|[0-9])(\w)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4}))$/;
	// !reg.test(value) ? false :true
	if (!reg.test(value)){
		return false
	}else{
		return true
	}
}

/**
 * 验证验证码
 */
export function validatacode(value){
	let reg = /[A-Za-z0-9]{6}/;
	// !reg.test(value) ? false :true
	if (!reg.test(value)){
		return false
	}else{
		return true
	}
}