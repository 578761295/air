<template>
	<div id="equipment-style">
		<el-row type="flex">
			<el-col :span="8" class="el-col-style">
				<div class="div-style" align="center">
					<h4>用户总设备</h4>
				</div>
				<h1 align="center" class="h1-style1">{{display.total}}台</h1>
			</el-col>
			<el-col :span="8" class="el-col-style">
				<div class="div-style" align="center">
					<h4 align="center">运行设备</h4>
				</div>
				<h1 align="center" class="h1-style1 h-green">{{display.running}}台</h1>
			</el-col>
			<el-col :span="8" class="el-col-style">
				<div class="div-style" align="center">
					<h4 align="center">已停止设备</h4>
				</div>
				<h1 align="center" class="h1-style1 h-red">{{display.stopped}}台</h1>
			</el-col>
		</el-row>
		<div class="div-table-style">
			<el-table :data="equipmentData" style="width: 100%" height="100%" @row-click="equipmentclick" :header-cell-style="{fontSize:'20px'}"
			 :cell-style="changeCellStyle">
				<el-table-column prop="tid" label="设备id" />
				<el-table-column prop="status" label="运行状态" />
				<el-table-column prop="address" label="地区" />
				<el-table-column prop="finalresponsetime" label="最后响应时间" />
			</el-table>
		</div>


		<div align="center">
			<el-button type="primary" @click="Onquery" class="el-button-style">检索设备</el-button>
			<el-button type="primary" @click="Ondialog = true" class="el-button-style">修改设备</el-button>
		</div>


		<el-dialog title="修改设备" :visible.sync="Ondialog">
			<h4 class="h4-style">(请确保是持有设备id，设备id理论上不允许修改，如需修改，请联系厂商)</h4>
			<el-form :model="dialogdata">
				<el-form-item label="设备id" :label-width="labelwidth">
					<el-select v-model="value" @change="changeValue" placeholder="请选择设备">
						<el-option v-for="item in equipmentData" :key="item.tid" :label="item.tid" :value="item.tid" />
					</el-select>
				</el-form-item>
				<el-form-item label="设备区域" :label-width="labelwidth">
					<el-input v-model="dialogdata.address" autocomplete="off" class="el-input-style" />
				</el-form-item>
			</el-form>
			<div slot="footer" class="dialog-footer">
				<el-button @click="Ondialog = false">取 消</el-button>
				<el-button type="primary" @click="Onchange">确 定</el-button>
			</div>
		</el-dialog>

	</div>
</template>

<script>
	import {
		saveData,
		readData
	} from "../../utils/storageUtils.js"
	import {
		ref,
		reactive
	} from '@vue/composition-api'
	import {
		request
	} from "../../utils/request.js"

	const display = reactive({
		total: 0,
		running: 0,
		stopped: 0
	})

	export default {
		name: 'consoleequipment',
		setup(props, {
			root
		}) {
			const Ondialog = ref(false)

			const dialogdata = reactive({
				tid: "",
				address: ""
			})

			const optionvalue = reactive({
				valuedata: ''
			})

			const equipmentData = reactive(readData('equipmentdata'))

			var equipmentdata = []

			const Onquery = (() => {
				var data = {
					requirement: 'onquery',
					mailbox: readData('currentuser'),
				}
				request({
					url: "/consoleequipment",
					data: data
				}).then(res => {
					if (res != false) {
						if (res.length < equipmentdata.length) {
							equipmentdata.forEach((row, index) => {
								equipmentData.splice(equipmentdata.length - index, 1)
							})
						}
						saveData('equipmentdata', res)
						equipmentdata = res
						equipmentdata.forEach((row, index) => {
							root.$set(equipmentData, index, {
								tid: row.tid,
								status: row.status,
								address: row.address,
								finalresponsetime: row.finalresponsetime
							})
						})
						root.$message({
							showClose: true,
							message: '检索完毕，已经是最新的设备表',
							type: 'success'
						})
					} else {
						root.$message({
							showClose: true,
							message: '请求用户设备表操作失败',
							type: 'warning'
						})
					}
				}, err => {
					root.$message({
						showClose: true,
						message: '请求服务器错误',
						type: 'error'
					})
					console.log("consoleequipment")
					console.log(err)
					console.log("consoleequipment")
				})
			})

			const equipmentclick = ((row) => {
				saveData('currentequipment', row.tid);
				root.$router.push({
					path: '/equipmenthome'
				})
			});

			const changeCellStyle = ((row) => {
				//列的label的名称
				if (row.column.label === "设备id") {
					return {
						cursor: 'pointer',
						color: 'blue',
						fontSize: '15px'
					} //修改的样式,cursor:pointer color:blue 
				}
			});

			const changeValue = (value => {
				optionvalue.valuedata = value
			})

			const Onchange = (() => {
				var data = {
					requirement: 'onchange',
					tid: optionvalue.valuedata,
					address: dialogdata.address
				}
				request({
					url: "/consoleequipment",
					data: data
				}).then(res => {
					if (res != false) {
						equipmentData.forEach((row, index) => {
							if (row.tid == optionvalue.valuedata) {
								root.$set(equipmentData, index, {
									tid: row.tid,
									status: row.status,
									address: dialogdata.address,
									finalresponsetime: row.finalresponsetime
								})
							}
						})
						root.$message({
							showClose: true,
							message: '修改设备成功',
							type: 'success'
						})
						dialogdata.address = "";
						Ondialog.value = false
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

			return {
				equipmentclick,
				changeCellStyle,
				Ondialog,
				labelwidth: '100px',
				Onchange,
				Onquery,
				dialogdata,
				equipmentData,
				value: '',
				changeValue,
				display
			}
		},

		mounted() {
			this.timer = setInterval(() => {
				var data = {
					requirement: "timer",
					mailbox: readData('currentuser'),
				}
				request({
					url: "/consoleequipment",
					data: data
				}).then(res => {
					if (res != false) {
						this.display.total = res.total
						this.display.running = res.running
						this.display.stopped = res.stopped
					} else {
						this.$message({
							showClose: true,
							message: '初始化请求服务器失败',
							type: 'warning'
						})
					}
				}, err => {
					this.$message({
						showClose: true,
						message: '请求服务器错误',
						type: 'error'
					})
					console.log("equipmenthome-timer")
					console.log(err)
					console.log("equipmenthome-timer")
				})
			}, 5000)

		},

		beforeDestroy() {
			if (this.timer) {
				clearInterval(this.timer); //关闭
			} //利用vue的生命周期函数
		}

	}
</script>

<style>
	#equipment-style {
		position: absolute;
		background-color: white;
		top: 20px;
		left: 20px;
		right: 20px;
		bottom: 20px;
		box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)
	}

	.div-table-style {
		margin-top: 30px;
		margin-left: 30px;
		margin-right: 30px;
		height: 400px;
	}

	.el-button-style {
		margin-top: 30px;
	}

	.el-input-style {
		width: 250px;
	}

	.h4-style {
		margin-top: -40px;
		margin-bottom: 30px;
	}

	.el-col-style {
		margin-top: 20px;
		margin-left: 20px;
		margin-right: 20px;
		margin-bottom: 20px;
		box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
		border-radius: 20px;
	}

	.div-style {
		border-radius: 20px;
		height: 40px;
		line-height: 40px;
		background-color: #424242;
		color: white;
	}

	.h1-style1 {
		height: 90px;
		line-height: 90px;
	}

	.h-green {
		color: green;
	}

	.h-red {
		color: red;
	}
</style>
