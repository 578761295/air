<template>
	<div id="superadministrtor-style">
		<div class="div-style">
			<el-row type="flex">
				<el-col :span="4">
					<h3 class="h3-style">账号:</h3>
				</el-col>
				<el-col :span="14">
					<el-input v-model="queryuser.mailbox" placeholder="请输入账号" prefix-icon="el-icon-search" maxlength=25 class="el-input-style" />
				</el-col>
				<el-col :span="4">
					<el-button type="primary" @click="Onquery">查询</el-button>
				</el-col>
			</el-row>
		</div>

		<div class="div-style">
			<el-table :data="tableData" style="width: 100%" border>
				<el-table-column prop="mailbox" label="用户id" />
				<el-table-column prop="password" label="密码" />
				<el-table-column prop="power" label="权限" />
			</el-table>
		</div>

		<div class="div-style">
			<el-row type="flex">
				<el-col :span="2" class="el-col-style" />
				<el-col :span="20" class="el-col-style">
					<el-button type="primary" @click="Onadd">添加管理</el-button>
					<el-button type="primary" @click="Ondel">删除管理</el-button>
					<el-button type="primary" @click="Onchangepassword">修改密码</el-button>
					<!-- 按下修改密码,显示出来,不按不显示 -->
					<el-input v-model="queryuser.password" placeholder="请输入密码" v-if='changepassword' maxlength=25 class="el-input-style el-input-style1"
					 show-password clearable />
					<el-button icon="el-icon-finished" v-if='changepassword' @click="Onchange" class="el-input-style1" circle />
				</el-col>
				<el-col :span="2" class="el-col-style" />
			</el-row>
		</div>
	</div>
</template>

<script>
	import {
		ref,
		reactive
	} from '@vue/composition-api'
	import {
		validatamailbox,
		stripscript
	} from "../../utils/validata.js"
	import {
		request
	} from "../../utils/request.js"
	export default {
		name: 'superadministrator',
		setup(props, {
			root
		}) {
			const changepassword = ref(false)

			const queryuser = reactive({
				mailbox: '',
				password: '',
			})

			const tableData = reactive([{
				mailbox: "xxx",
				password: "xxx",
				power: "xxx"
			}])

			const tabledata = reactive([{
				mailbox: "",
				password: "",
				power: ""
			}])

			const Onquery = (() => {
				if (queryuser.mailbox === '') {
					root.$message({
						showClose: true,
						message: '邮箱不能为空',
						type: 'error'
					})
				} else if (!validatamailbox(queryuser.mailbox)) {
					root.$message({
						showClose: true,
						message: '邮箱格式错误',
						type: 'warning'
					})
				} else {
					var data = {
						requirement: 'onquery',
						mailbox: queryuser.mailbox
					}
					request({
						url: "/superadministrator",
						data: data
					}).then(res => {
						if (res != false) {
							// {mailbox: "123456789@qq.com", password: "123abc", power: "r-x"}
							tabledata.mailbox = res.mailbox;
							tabledata.password = res.password;
							tabledata.power = res.power;
							root.$set(tableData, 0, {
								'mailbox': tabledata.mailbox,
								'password': tabledata.password,
								'power': tabledata.power
							})
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
						console.log("superadministrator-Onquery")
						console.log(err)
						console.log("superadministrator-Onquery")
					})
				}
			})

			//tableData添加 w，保存数据库
			const Onadd = (() => {
				var data = {
					requirement: 'onadddel',
					mailbox: tabledata.mailbox,
					power: "rwx"
				}
				request({
					url: "/superadministrator",
					data: data
				}).then(res => {
					if (res != false) {
						tabledata.power = "rwx"
						root.$set(tableData, 0, {
							'mailbox': tabledata.mailbox,
							'password': tabledata.password,
							'power': "rwx"
						})
						root.$message({
							showClose: true,
							message: '添加用户权限成功',
							type: 'success'
						})
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
					console.log("superadministrator-Onadd")
					console.log(err)
					console.log("superadministrator-Onadd")
				})
			})

			//tableData删除 w，保存数据库
			const Ondel = (() => {
				var data = {
					requirement: 'onadddel',
					mailbox: tabledata.mailbox,
					power: "r-x"
				}
				request({
					url: "/superadministrator",
					data: data
				}).then(res => {
					if (res != false) {
						tabledata.power = "r-x"
						root.$set(tableData, 0, {
							'mailbox': tabledata.mailbox,
							'password': tabledata.password,
							'power': "r-x"
						})
						root.$message({
							showClose: true,
							message: '删除用户权限成功',
							type: 'success'
						})
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
					console.log("superadministrator-Ondel")
					console.log(err)
					console.log("superadministrator-Ondel")
				})
			})

			const Onchangepassword = (() => {
				changepassword.value = !changepassword.value
			})

			const Onchange = (() => {
				queryuser.password = stripscript(queryuser.password)
				if (queryuser.password === '') {
					root.$message({
						showClose: true,
						message: '新密码不能为空',
						type: 'error'
					})
				} else if (queryuser.password.length < 8 || queryuser.password.length > 20) {
					root.$message({
						showClose: true,
						message: '新密码为8-20位字母、数字、特殊字符$@%#',
						type: 'warning'
					})
				} else {
					var data = {
						requirement: 'onchange',
						mailbox: tabledata.mailbox,
						password: queryuser.password
					}
					request({
						url: "/superadministrator",
						data: data
					}).then(res => {
						if (res != false) {
							tabledata.password = queryuser.password;
							root.$set(tableData, 0, {
								'mailbox': tabledata.mailbox,
								'password': tabledata.password,
								'power': tabledata.power
							})
							root.$message({
								showClose: true,
								message: '修改密码成功',
								type: 'success'
							})
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
						console.log("superadministrator-Onchange")
						console.log(err)
						console.log("superadministrator-Onchange")
					})
				}

			})

			return {
				tableData,
				queryuser,
				changepassword,
				Onquery,
				Onadd,
				Ondel,
				Onchangepassword,
				Onchange
			}
		}
	}
</script>

<style lang="scss" scoped>
	#superadministrtor-style {
		position: absolute;
		top: 20px;
		left: 20px;
		right: 20px;
		box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)
	}

	.div-style {
		margin: 30px;
	}

	.el-col-style {
		text-align: center;
	}

	.el-input-style {
		width: 250px;
	}

	.el-input-style1 {
		margin-left: 10px;
	}

	.h3-style {
		text-align: right;
		margin-right: 10px;
		line-height: 40px;
	}
</style>
