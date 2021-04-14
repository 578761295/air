<template>
	<div id="superadministrtor-style">
		<div class="div-style-user">
			<el-row type="flex">
				<el-col :span="2">
					<h3 class="h3-style">账号:</h3>
				</el-col>
				<el-col :span="8">
					<el-input v-model="queryuser.mailbox" placeholder="请输入账号" prefix-icon="el-icon-user" maxlength=25 class="el-input-style"
					 clearable />
				</el-col>
				<el-col :span="2">
					<h3 class="h3-style">密码:</h3>
				</el-col>
				<el-col :span="8">
					<el-input v-model="queryuser.password" placeholder="请输入密码" prefix-icon="el-icon-lock" maxlength=25 class="el-input-style"
					 show-password clearable />
				</el-col>
				<el-col :span="4">
					<el-button type="primary" @click="Onquery('queryuser')">登录</el-button>
				</el-col>
			</el-row>
		</div>

		<div class="div-table-style">
			<el-table :data="tableData" style="width: 100%" height="100%" @selection-change="handleSelectionChange" border>
				<el-table-column type="selection" width="55" />
				<el-table-column prop="tid" label="设备id" />
				<el-table-column prop="address" label="设备地区" />
				<el-table-column prop="tkey" label="设备密钥" />
				<el-table-column fixed="right" label="操作" width="120">
					<template slot-scope="scope">
						<el-button @click.native.prevent="deleteRow(scope.$index, tableData)" type="text" size="small">
							删除设备
						</el-button>
					</template>
				</el-table-column>
			</el-table>
		</div>

		<div class="div-style-user">
			<el-row type="flex">
				<el-col :span="2" class="el-col-style" />
				<el-col :span="20" class="el-col-style">
					<el-button type="primary" @click="Ondialog = true" class="el-button-style">添加设备</el-button>
					<el-popconfirm confirm-button-text='确认删除' cancel-button-text='取消' @confirm="Ondel" icon="el-icon-info" icon-color="red"
					 title="是否删除选中的设备？">
						<el-button slot="reference">批量删除设备</el-button>
					</el-popconfirm>
				</el-col>
				<el-col :span="2" class="el-col-style" />
			</el-row>

			<el-dialog title="添加设备" :visible.sync="Ondialog">
				<h4 class="h4-style">(请确保设备id是唯一的,如添加失败可能设备id不唯一,请联系厂商)</h4>
				<el-form :model="dialogdata">
					<el-form-item label="设备id" :label-width="labelwidth">
						<el-input v-model="dialogdata.tid" autocomplete="off" class="el-input-style" />
					</el-form-item>
					<el-form-item label="设备区域" :label-width="labelwidth">
						<el-input v-model="dialogdata.address" autocomplete="off" class="el-input-style" />
					</el-form-item>
					<el-form-item label="设备密钥" :label-width="labelwidth">
						<el-input v-model="dialogdata.tkey" autocomplete="off" class="el-input-style" />
					</el-form-item>
				</el-form>
				<div slot="footer" class="dialog-footer">
					<el-button @click="Ondialog = false">取 消</el-button>
					<el-button type="primary" @click="Onadd">确 定</el-button>
				</div>
			</el-dialog>
		</div>
	</div>
</template>

<script>
	import {
		ref,
		reactive
	} from '@vue/composition-api'
	import {
		validatamailbox
	} from "../../utils/validata.js"
	import {
		request
	} from "../../utils/request.js"
	export default {
		name: 'useradministrator',
		setup(props, {
			root
		}) {
			const queryuser = reactive({
				mailbox: '',
				password: '',
			})

			const queryuserdata = reactive({
				mailbox: ''
			})

			const tableData = reactive([{
				tid: "xxx",
				address: "xxx",
				tkey: "xxx"
			}])

			var tabledata = []

			const multipleSelection = reactive([])

			const dialogdata = reactive({
				tid: "",
				address: "",
				tkey: ""
			})

			const Onquery = (() => {
				if (queryuser.mailbox === '' || queryuser.password === '') {
					root.$message({
						showClose: true,
						message: '邮箱或者密码不能为空',
						type: 'error'
					})
				} else if (!validatamailbox(queryuser.mailbox)) {
					root.$message({
						showClose: true,
						message: '邮箱格式错误',
						type: 'warning'
					})
				} else if (queryuser.password.length < 8 || queryuser.password.length > 20) {
					root.$message({
						showClose: true,
						message: '密码格式错误',
						type: 'warning'
					})
				} else {
					var data = {
						requirement: 'onquery',
						mailbox: queryuser.mailbox,
						password: queryuser.password
					}
					request({
						url: "/useradministrator",
						data: data
					}).then(res => {
						if (res != false) {
							queryuserdata.mailbox = queryuser.mailbox
							if (res.length < tabledata.length) {
								tabledata.forEach((row, index) => {
									console.log(index)
									tableData.splice(tabledata.length - index, 1)
								})
							}
							tabledata = res
							tabledata.forEach((row, index) => {
								root.$set(tableData, index, {
									'tid': row.tid,
									'address': row.address,
									'tkey': row.tkey
								})
							})
						} else {
							root.$message({
								showClose: true,
								message: '请输入正确的账号密码',
								type: 'error'
							})
						}
					}, err => {
						root.$message({
							showClose: true,
							message: '请求服务器错误',
							type: 'error'
						})
						console.log("useradministrator-Onquery")
						console.log(err)
						console.log("useradministrator-Onquery")
					})
				}
			})

			const deleteRow = ((index, row) => {
				// 	//对数据库操作，不需要确认是否删除
				var data = {
					requirement: 'deleteRow',
					mailbox: queryuserdata.mailbox,
					tid: row[index].tid
				}
				request({
					url: "/useradministrator",
					data: data
				}).then(res => {
					if (res != false) {
						row.splice(index, 1);
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
					console.log("useradministrator-deleteRow")
					console.log(err)
					console.log("useradministrator-deleteRow")
				})
			});

			const Onadd = (() => {
				var data = {
					requirement: 'onadd',
					mailbox: queryuserdata.mailbox,
					tid: dialogdata.tid,
					address: dialogdata.address,
					tkey: dialogdata.tkey
				}
				request({
					url: "/useradministrator",
					data: data
				}).then(res => {
					if (res != false) {
						tabledata.push({
							tid: dialogdata.tid,
							address: dialogdata.address,
							tkey: dialogdata.tkey
						})
						root.$set(tableData, tableData.length, {
							tid: dialogdata.tid,
							address: dialogdata.address,
							tkey: dialogdata.tkey
						})
						root.$message({
							showClose: true,
							message: '添加设备成功',
							type: 'success'
						})
						dialogdata.tid = "";
						dialogdata.address = "";
						dialogdata.tkey = "";
					} else {
						root.$message({
							showClose: true,
							message: '请求服务器失败',
							type: 'warning'
						})
					}
				}, err => {
					root.$message({
						showClose: true,
						message: '请求服务器错误',
						type: 'error'
					})
					console.log("useradministrator-Onadd")
					console.log(err)
					console.log("useradministrator-Onadd")
				})
			})

			const handleSelectionChange = ((row) => {
				multipleSelection.value = row
			})

			//tableData删除 w，保存数据库
			const Ondel = (() => {
				var data = {
					requirement: 'ondel',
					mailbox: queryuserdata.mailbox,
					data: multipleSelection.value
				}
				request({
					url: "/useradministrator",
					data: data,

				}).then(res => {
					if (res != false) {
						multipleSelection.value.forEach(row => {
							tableData.forEach((rows, indexs) => {
								if (row.tid == rows.tid) {
									tableData.splice(indexs, 1)
								}
							})
						})
						tabledata = tableData
						root.$message({
							showClose: true,
							message: '批量删除设备成功',
							type: 'success'
						})
					} else {
						root.$message({
							showClose: true,
							message: '请求服务器失败',
							type: 'warning'
						})
					}
				}, err => {
					root.$message({
						showClose: true,
						message: '请求服务器错误',
						type: 'error'
					})
					console.log("useradministrator-Ondel")
					console.log(err)
					console.log("useradministrator-Ondel")
				})
			})

			return {
				tableData,
				queryuser,
				dialogdata,
				elpopoverstatus: false,
				Onquery,
				deleteRow,
				handleSelectionChange,
				Ondialog: false,
				Onadd,
				Ondel,
				labelwidth: '100px'
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

	.div-style-user {
		margin: 30px;
	}

	.div-table-style {
		margin-top: 30px;
		margin-left: 30px;
		margin-right: 30px;
		height: 400px;
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

	.el-button-style {
		margin-right: 30px;
	}

	.h3-style {
		text-align: right;
		margin-right: 10px;
		line-height: 40px;
	}

	.h4-style {
		margin-top: -40px;
		margin-bottom: 30px;
	}
</style>
