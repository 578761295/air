<template>
	<div id="personal-style">
		<el-row>
			<h3 class="personal-el-col-style">基本信息</h3>
		</el-row>
		<el-row type="flex">
			<el-col :span="12" class="personal-el-col-style">
				<el-row type="flex" class="personal-el-row-style">
					<el-col :span="5">账号昵称</el-col>
					<el-col :span="18" v-if='!nickinput'>{{getinput.nick}}</el-col>
					<el-input size="small" placeholder="请输入昵称" v-if='nickinput' v-model="getinput.nick" clearable />
					<el-button size="small" icon="el-icon-edit" v-if='!nickinput' @click="Nickinput()" circle />
					<el-button size="small" icon="el-icon-finished" v-if='nickinput' @click="Getnick()" circle />
				</el-row>
				<el-row type="flex" class="personal-el-row-style">
					<el-col :span="5">账号id</el-col>
					<el-col :span="18">{{userid}}</el-col>
				</el-row>
			</el-col>
			<div class="verticalBar"></div>
			<el-col :span="12" class="personal-el-col-style">
				<el-row type="flex" class="personal-el-row-style">
					<el-col :span="5">联系手机</el-col>
					<el-col :span="18" v-if='!phoneinput'>{{getinput.phone}}</el-col>
					<el-input size="small" placeholder="请输入手机号" v-if='phoneinput' v-model="getinput.phone" clearable />
					<el-button size="small" icon="el-icon-edit" v-if='!phoneinput' @click="Phoneinput()" circle />
					<el-button size="small" icon="el-icon-finished" v-if='phoneinput' @click="Getphone()" circle />
				</el-row>
				<el-row type="flex" class="personal-el-row-style">
					<el-col :span="5">联系地址</el-col>
					<el-col :span="18" v-if='!addressinput'>{{getinput.address}}</el-col>
					<el-input size="small" placeholder="请输入地址" v-if='addressinput' v-model="getinput.address" clearable />
					<el-button size="small" icon="el-icon-edit" v-if='!addressinput' @click="Addressinput()" circle />
					<el-button size="small" icon="el-icon-finished" v-if='addressinput' @click="Getaddress()" circle />
				</el-row>
				<el-row type="flex" class="personal-el-row-style">
					<el-col :span="5">联系邮箱</el-col>
					<el-col :span="18" v-if='!mailinput'>{{getinput.mail}}</el-col>
					<el-input size="small" placeholder="请输入邮箱" v-if='mailinput' v-model="getinput.mail" clearable />
					<el-button size="small" icon="el-icon-edit" v-if='!mailinput' @click="Mailinput()" circle />
					<el-button size="small" icon="el-icon-finished" v-if='mailinput' @click="Getmail()" circle />
				</el-row>
			</el-col>
		</el-row>

	</div>
</template>

<script>
	import {
		readData,
		saveData
	} from "../../utils/storageUtils.js"
	import {
		request
	} from "../../utils/request.js"
	import {
		reactive,
		ref
	} from '@vue/composition-api'
	export default {
		name: 'consolepersonal',
		setup(props, {
			root
		}) {
			const nickinput = ref(false)
			const phoneinput = ref(false)
			const addressinput = ref(false)
			const mailinput = ref(false)

			const getinput = reactive({
				nick: readData('information').nick != null ? readData('information').nick : '',
				phone: readData('information').phone != null ? readData('information').phone : '',
				address: readData('information').address != null ? readData('information').address : '',
				mail: readData('information').mail != null ? readData('information').mail : ''
			})

			const Nickinput = (() => {
				nickinput.value = true
			})
			const Phoneinput = (() => {
				phoneinput.value = true
			})
			const Addressinput = (() => {
				addressinput.value = true
			})
			const Mailinput = (() => {
				mailinput.value = true
			})

			const Getnick = (() => {
				if (readData('currentuser') != '578761295@qq.com') {
					var data = {
						mailbox: readData('currentuser'),
						data: {
							nick: getinput.nick,
							phone: getinput.phone,
							address: getinput.address,
							mail: getinput.mail
						}
					}
					request({
						url: "/consolepersonal",
						data: data
					}).then(res => {
						if (res != false) {
							saveData('information', data.data)
							nickinput.value = false
						} else {
							root.$message({
								showClose: true,
								message: '请求服务器操作失败',
								type: 'warning'
							})
						}
					}, err => {
						root.$message({
							showClose: true,
							message: '请求服务器错误',
							type: 'error'
						})
						console.log("consolepersonal-Getnick")
						console.log(err)
						console.log("consolepersonal-Getnick")
					})
				}
			})

			const Getphone = (() => {
				var data = {
					mailbox: readData('currentuser'),
					data: {
						nick: getinput.nick,
						phone: getinput.phone,
						address: getinput.address,
						mail: getinput.mail
					}
				}
				request({
					url: "/consolepersonal",
					data: data
				}).then(res => {
					if (res != false) {
						saveData('information', data.data)
						phoneinput.value = false
					} else {
						root.$message({
							showClose: true,
							message: '请求服务器操作失败',
							type: 'warning'
						})
					}
				}, err => {
					root.$message({
						showClose: true,
						message: '请求服务器错误',
						type: 'error'
					})
					console.log("consolepersonal-Getphone")
					console.log(err)
					console.log("consolepersonal-Getphone")
				})
			})

			const Getaddress = (() => {
				var data = {
					mailbox: readData('currentuser'),
					data: {
						nick: getinput.nick,
						phone: getinput.phone,
						address: getinput.address,
						mail: getinput.mail
					}
				}
				request({
					url: "/consolepersonal",
					data: data
				}).then(res => {
					if (res != false) {
						saveData('information', data.data)
						addressinput.value = false
					} else {
						root.$message({
							showClose: true,
							message: '请求服务器操作失败',
							type: 'warning'
						})
					}
				}, err => {
					root.$message({
						showClose: true,
						message: '请求服务器错误',
						type: 'error'
					})
					console.log("consolepersonal-Getaddress")
					console.log(err)
					console.log("consolepersonal-Getaddress")
				})
			})

			const Getmail = (() => {
				var data = {
					mailbox: readData('currentuser'),
					data: {
						nick: getinput.nick,
						phone: getinput.phone,
						address: getinput.address,
						mail: getinput.mail
					}
				}
				request({
					url: "/consolepersonal",
					data: data
				}).then(res => {
					if (res != false) {
						saveData('information', data.data)
						mailinput.value = false
					} else {
						root.$message({
							showClose: true,
							message: '请求服务器操作失败',
							type: 'warning'
						})
					}
				}, err => {
					root.$message({
						showClose: true,
						message: '请求服务器错误',
						type: 'error'
					})
					console.log("consolepersonal-Getmail")
					console.log(err)
					console.log("consolepersonal-Getmail")
				})
			})

			return {
				getinput,
				nickinput,
				Nickinput,
				Getnick,
				userid: readData('currentuser'),
				phoneinput,
				Phoneinput,
				Getphone,
				addressinput,
				Addressinput,
				Getaddress,
				mailinput,
				Mailinput,
				Getmail
			}
		}
	}
</script>

<style lang="scss" scoped>
	#personal-style {
		position: absolute;
		background-color: white;
		top: 20px;
		left: 20px;
		right: 20px;
		box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)
	}

	.verticalBar {
		border-left: 2px solid #e5e5e5;
	}

	.personal-el-col-style {
		margin: 30px;
	}

	.personal-el-row-style {
		margin-bottom: 10px;
	}
</style>
