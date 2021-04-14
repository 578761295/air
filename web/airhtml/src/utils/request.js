import axios from 'axios';

// axios用于浏览器与nodejs中的请求

export function request(config) {
	// 创建实例instance对服务器的URl进行请求
	const instance = axios.create({
		method: 'post',
		baseURL: "http://106.55.27.102:5000",
		// baseURL: "http://127.0.0.1:5000",
		timeout: 10000
	});
	// interceptors是一个响应拦截器。拦截没有用的信息，并返回所需要的数据
	instance.interceptors.response.use(res => {
		// console.log("拦截器拦截的结果", res);
		return res.data;
	}, err => {
		console.log(err)
		return false;
	})
	return instance(config);
}
