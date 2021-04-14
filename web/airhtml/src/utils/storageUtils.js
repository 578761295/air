/*
 * 读取数据
 * key：数据对象的key
 */
export function readData(key) {
	if(localStorage.getItem(key) != null)
		return JSON.parse(localStorage.getItem(key))
	else
		return ''
}
/*
 * 保存数据
 * key：数据对象的key
 * data：要保存的数据
 */
export function saveData(key, data) {
	localStorage.setItem(key, JSON.stringify(data))
}
/*
 * 删除数据
 * key：数据对象的key
 */
export function removeData(key) {
	localStorage.removeItem(key)
}

// 存数据
// localStorage.setItem('userName', '张三')；
// localStorage.userName="张三"；
// 读数据
// localStorage.getItem('userName');
// var username = localStorage.userName
// 删除数据
// localStorage.removeItem('userName')

