<template>
	<div id="login">
		<div class="login-warp">
			<div class="menu-tab">
				<li v-for="item in menulable" :key="item.id" :class="{'current':item.current}" @click="ToggleMenu(item)">{{item.txt}}</li>
			</div>
			<el-form :model="logintable" :rules="rules" ref="logintable" label-width="70px" size='medium' status-icon>
				<el-form-item label="邮箱" prop="mailboxinput">
					<el-input type="text" v-model="logintable.mailboxinput" maxlength="25" clearable />
				</el-form-item>
				<el-row :gutter="5" v-show="menumodel === 'toregister'">
					<el-form-item label="验证码" prop="code">
						<el-col :span="14">
							<el-input v-model="logintable.code" minlength="6" maxlength="6" clearable />
						</el-col>
						<el-col :span="6">
							<el-button type="success" @click="GetCode()" :disabled="codebutton.status">{{codebutton.text}}</el-button>
						</el-col>
					</el-form-item>
				</el-row>
				<el-form-item label="密码" prop="passwordinput" v-show="loginmodel == 'toregister'? toregisterstatus :true">
					<el-input type="password" v-model="logintable.passwordinput" maxlength="25" show-password clearable />
				</el-form-item>
				<el-form-item label="确认密码" prop="passwordsinput" v-show="menumodel == 'toregister'? toregisterstatus :false">
					<el-input type="password" v-model="logintable.passwordsinput" maxlength="25" show-password clearable />
				</el-form-item>
				<div>
					<el-button type="primary" @click="Login('logintable')" class="login-btn" v-show="loginmodel === 'tologin'">登录</el-button>
				</div>
				<div>
					<el-button type="primary" @click="Register('logintable')" class="login-btn" v-show="menumodel === 'toregister'">注册</el-button>
				</div>
			</el-form>
			<div align="right">
				<el-link type="text" :underline="false" @click="openOndialog">忘记密码</el-link>
			</div>
		</div>

		<el-dialog title="修改密码" :visible.sync="Ondialog" :show-close="false" :close-on-click-modal="false">
			<el-form :model="logintable" :rules="rules" ref="logintable" label-width="70px" status-icon>
				<el-form-item label="邮箱" prop="mailboxinput" style="width: 450px;">
					<el-input type="text" v-model="logintable.mailboxinput" maxlength="25" clearable />
				</el-form-item>
				<el-row :gutter="5" style="width: 500px;">
					<el-form-item label="验证码" prop="code">
						<el-col :span="14">
							<el-input v-model="logintable.code" minlength="6" maxlength="6" clearable />
						</el-col>
						<el-col :span="6">
							<el-button type="success" @click="GetCode()" :disabled="codebutton.status">{{codebutton.text}}</el-button>
						</el-col>
					</el-form-item>
				</el-row>
				<el-form-item label="密码" prop="passwordinput" style="width: 450px;" v-show="Ondialogstatus">
					<el-input type="password" v-model="logintable.passwordinput" maxlength="25" show-password clearable />
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="openOndialog">取 消</el-button>
				<el-button type="primary" @click="Onchange('logintable')">修改密码</el-button>
			</div>
		</el-dialog>
	</div>
</template>

<script>
	import {
		reactive,
		ref
	} from '@vue/composition-api'
	import {
		stripscript,
		validatamailbox,
		validatacode
	} from "../../utils/validata.js"
	import {
		request
	} from "../../utils/request.js"
	import {
		saveData,
		readData
	} from "../../utils/storageUtils.js"
	export default {
		name: 'login',
		setup(props, {
			refs,
			root
		}) {
			var validatemailboxinput = (rule, value, callback) => {
				if (value === '') {
					callback(new Error('邮箱不能为空'));
				} else if (!validatamailbox(value)) {
					callback(new Error('邮箱格式错误'));
				} else {
					callback(); //返回一个true
				}
			};
			var validatepasswordinput = (rule, value, callback) => {
				logintable.passwordinput = stripscript(value)
				value = logintable.passwordinput
				if (value === '') {
					callback(new Error('密码不能为空'));
				} else if (value.length < 8 | value.length > 20) {
					callback(new Error('密码为8-20位字母、数字、特殊字符$@%#'));
				} else {
					callback();
				}
			};
			var validatepasswordsinput = (rule, value, callback) => {
				// 模块在'tologin'，跳过
				if (loginmodel.value === 'tologin' && Ondialogstatus.value != true) {
					callback();
				}
				logintable.passwordsinput = stripscript(value)
				value = logintable.passwordsinput
				if (value === '') {
					callback(new Error('确认密码不能为空'));
				} else if (value != logintable.passwordinput) {
					callback(new Error('确认密码与密码不一致，请重新输入'));
				} else {
					callback();
				}
			};
			var validateCode = (rule, value, callback) => {
				if (loginmodel.value === 'tologin') {
					callback();
				}
				if (value === '') {
					callback(new Error('验证码不能为空'));
				} else if (!validatacode(value)) {
					callback(new Error('验证码格式有误'));
				} else {
					callback();
				}
			};

			const Ondialog = ref(false)
			const toregisterstatus = ref(false)
			const Ondialogstatus = ref(false)
			const dialogstatus = ref(false)

			const menulable = reactive([{
					txt: '登录',
					current: true,
					type: 'tologin'
				},
				{
					txt: '注册',
					current: false,
					type: 'toregister'
				}
			])

			const loginmodel = ref('tologin')
			const menumodel = ref('tologin')

			const codebutton = reactive({
				status: false,
				text: '获取验证码'
			})

			const timer = ref(null)
			const timer1 = ref(null)

			const logintable = reactive({
				mailboxinput: '',
				passwordinput: '',
				passwordsinput: '',
				code: ''
			})

			//表单的验证
			const rules = reactive({
				// validator:失去焦点的触发
				mailboxinput: [{
					validator: validatemailboxinput,
					trigger: 'blur'
				}],
				passwordinput: [{
					validator: validatepasswordinput,
					trigger: 'blur'
				}],
				passwordsinput: [{
					validator: validatepasswordsinput,
					trigger: 'blur'
				}],
				code: [{
					validator: validateCode,
					trigger: 'blur'
				}]
			})

			//点击登录注册高光
			const ToggleMenu = (data => {
				menulable.forEach(elem => {
					elem.current = false
				});
				data.current = true
				loginmodel.value = data.type
				menumodel.value = data.type
				toregisterstatus.value = false
				// 获取验证码
				clearInterval(timer.value)
				clearInterval(timer1.value)
				codebutton.status = false
				codebutton.text = '获取验证码'
				refs.logintable.resetFields();
			})

			// 获取验证码
			const GetCode = (() => {
				// 请求验证码
				if (validatamailbox(logintable.mailboxinput) == true) {
					var data = {
						requirement: dialogstatus.value != true ? 'registercode' : 'forgetcode',
						mailbox: logintable.mailboxinput,
					}
					codebutton.status = true
					codebutton.text = '正在发送中'
					timer.value = setTimeout(() => {
						request({
							url: "/login",
							data: data
						}).then(res => {
							if (res != false) {
								if (loginmodel.value == 'toregister' && dialogstatus.value != true) {
									toregisterstatus.value = true
								}
								if (dialogstatus.value == true) {
									Ondialogstatus.value = true
								}
								saveData('coderesult', res)
								root.$message({
									showClose: true,
									message: '验证码已发送',
									type: 'success',
								})
							} else {
								root.$message({
									showClose: true,
									message: '获取邮箱验证码失败，用户可能已存在',
									type: 'warning',
								})
							}
						}, err => {
							root.$message({
								showClose: true,
								message: '请求服务器错误',
								type: 'error',
							})
							console.log("login-Code")
							console.log(err)
							console.log("login-Code")
						})
						// 调用定时器，倒计时
						countDown(50)
					}, 10000)
				} else {
					root.$message({
						showClose: true,
						message: '邮箱不能为空',
						type: 'warning',
					});
					return false;
				}
			})

			// 倒计时
			const countDown = ((num) => {
				// setTimeout 只执行一次 clearTimeout(变量)
				// setInterval 不断执行，需要条件停止 clearInterval(变量)
				let time = num
				timer1.value = setInterval(() => {
					if (time === 0) {
						clearInterval(timer.value)
						clearInterval(timer1.value)
						codebutton.status = false
						codebutton.text = '  重新获取'
					} else {
						codebutton.text = `倒计时 ${time} 秒`
					}
					time--
				}, 1000)
			})

			// 登录，重新判断账号密码验证码类型是否符合，符合则请求
			// this.$refs[formName].validate()   检查该formName上添加的表单验证是否正确
			const Login = (formName => {
				refs[formName].validate((valid) => {
					if (valid) {
						var data = {
							requirement: 'login',
							mailbox: logintable.mailboxinput,
							password: logintable.passwordinput,
						}
						request({
							url: "/login",
							data: data
						}).then(res => {
							if (res != false) {
								saveData('currentuser', logintable.mailboxinput);
								saveData('currentpower', res.power)
								saveData('information', res.information)
								root.$router.push({
									path: '/console'
								})
							} else {
								root.$message({
									showClose: true,
									message: '请确认用户密码是否正确',
									type: 'warning',
								})
							}
						}, err => {
							root.$message({
								showClose: true,
								message: '请求服务器错误',
								type: 'error',
							})
							console.log("login-Login")
							console.log(err)
							console.log("login-Login")
						})
					} else {
						root.$message({
							showClose: true,
							message: '请确认输入格式是否符合',
							type: 'warning',
						})
						return false;
					}
				});
			})

			// 注册
			const Register = (formName => {
				refs[formName].validate((valid) => {
					if (valid) {
						if (logintable.passwordinput == logintable.passwordsinput && logintable.code == readData('coderesult')) {
							var data = {
								requirement: 'register',
								mailbox: logintable.mailboxinput,
								password: logintable.passwordinput,
							}
							request({
								url: "/login",
								data: data
							}).then(res => {
								if (res != false) {
									saveData('currentuser', logintable.mailboxinput);
									saveData('currentpower', 'r-x')
									saveData('information', {})
									root.$router.push({
										path: '/console'
									})
								} else {
									root.$message({
										showClose: true,
										message: '请确认用户密码是否正确',
										type: 'warning',
									})
								}
							}, err => {
								root.$message({
									showClose: true,
									message: '请求服务器错误',
									type: 'error',
								})
								console.log("login-Register")
								console.log(err)
								console.log("login-Register")
							})
						} else {
							root.$message({
								showClose: true,
								message: '请确认密码或者验证码是否正确',
								type: 'warning',
							})
						}
					} else {
						root.$message({
							showClose: true,
							message: '请确认输入格式是否符合',
							type: 'warning',
						})
						return false;
					}
				});
			})

			//忘记密码
			const Onchange = (formName => {
				refs[formName].validate((valid) => {
					if (valid) {
						if (logintable.code == readData('coderesult')) {
							var data = {
								requirement: 'forget',
								mailbox: logintable.mailboxinput,
								password: logintable.passwordinput,
							}
							request({
								url: "/login",
								data: data
							}).then(res => {
								if (res != false) {
									root.$message({
										showClose: true,
										message: '修改密码成功',
										type: 'success',
									})
								} else {
									root.$message({
										showClose: true,
										message: '请求修改密码失败',
										type: 'warning',
									})
								}
							}, err => {
								root.$message({
									showClose: true,
									message: '请求修改密码错误',
									type: 'error',
								})
								console.log("login-Onchange")
								console.log(err)
								console.log("login-Onchange")
							})
						} else {
							root.$message({
								showClose: true,
								message: '请确认验证码是否正确！！',
								type: 'error',
							})
						}
					} else {
						root.$message({
							showClose: true,
							message: '请确认输入格式是否符合',
							type: 'warning',
						})
						return false;
					}
				});
			})

			const openOndialog = (() => {
				clearInterval(timer.value)
				clearInterval(timer1.value)
				codebutton.status = false
				codebutton.text = '获取验证码'
				refs.logintable.resetFields();
				dialogstatus.value = !dialogstatus.value
				Ondialog.value = !Ondialog.value
				if (Ondialog.value == false) {
					Ondialogstatus.value = false
				}
				toregisterstatus.value = false
			})

			return {
				menulable,
				loginmodel,
				menumodel,
				codebutton,
				logintable,
				rules,
				ToggleMenu,
				GetCode,
				Login,
				Register,
				Ondialog,
				Onchange,
				toregisterstatus,
				Ondialogstatus,
				openOndialog
			}
		},
	}
</script>

<style lang="scss" scoped>
	#login {
		position: absolute;
		height: 100%;
		width: 100%;
		background: url(../../assets/login.jpeg);
		background-size: 100% 100%;
	}

	.login-warp {
		background: #B3D8FF;
		position: absolute;
		width: 350px;
		// height: 400px;
		top: 50%;
		left: 50%;
		-webkit-transform: translate(-50%, -50%);
		-moz-transform: translate(-50%, -50%);
		-ms-transform: translate(-50%, -50%);
		-o-transform: translate(-50%, -50%);
		transform: translate(-50%, -50%);
		border-radius: 15px;
		border: 1px solid #EAEAEA;
		padding: 15px 15px 15px 15px;
		box-shadow: 0 0 25px #cac6c6; // 阴影
	}

	.menu-tab {
		text-align: center;
		padding: 0px 0px 15px 0px;

		//li标签样式
		li {
			display: inline-block;
			width: 100px;
			line-height: 36px;
			font-size: 14px;
			color: #fff;
			border-radius: 2px;
			//指针变手势
			cursor: pointer;
		}

		//登录背景样式
		.current {
			background-color: rgba(85, 170, 255, 1.0);
		}
	}

	.login-btn {
		width: 100%;
	}
</style>
