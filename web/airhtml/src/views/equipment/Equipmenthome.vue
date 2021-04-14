<template>
	<div id="equipment-style">
		<el-row type="flex">
			<el-page-header id="lks" @back="goBack" class="el-style" />
			<label class="label-style">{{ getequipment }}</label>
		</el-row>
		<div class="el-style">
			<el-row type="flex">
				<el-col :span="6" class="el-col-style">
					<div class="div-style">
						<h4 class="h4-style1">实时天气</h4>
					</div>
					<div align="center">
						<h5 class="h5-style1">{{data.date}}</h5>
						<h5 class="h5-style1">{{data.address}}</h5>
						<h3>温度<i class="el-icon-odometer" />
							{{data.temperature}} &#176;C</h3>
						<h3>湿度<i class="el-icon-odometer" />
							{{data.humidity}} %</h3>
					</div>
				</el-col>
				<el-col class="el-col-width-style" />
				<el-col :span="18" class="el-col-style">
					<div class="div-style">
						<h4 class="h4-style1">环境质量</h4>
					</div>
					<el-row type="flex">
						<el-col :span="8">
							<div id="pm25" style="height: 150px" />
						</el-col>
						<el-col :span="8">
							<div id="hcho" style="height: 150px" />
						</el-col>
						<el-col :span="8">
							<div id="tvoc" style="height: 150px" />
						</el-col>
					</el-row>
				</el-col>
			</el-row>
		</div>

		<div class="div-style1">
			<el-button-group>
				<el-button icon="el-icon-date" @click="ononeday">一天</el-button>
				<el-button icon="el-icon-date" @click="ononeweek">一周</el-button>
				<!-- <el-button icon="el-icon-date" @click="ononemonth">一个月</el-button> -->
			</el-button-group>
		</div>

		<div id="linechart" class="div-style2" style="height: 500px" />

	</div>
</template>

<script>
	import {
		ref,
		reactive
	} from '@vue/composition-api'
	import { /*saveData,*/
		readData
	} from "../../utils/storageUtils.js"
	import {
		request
	} from "../../utils/request.js"
	import * as echarts from 'echarts';

	const data = reactive({
		date: "------",
		address: "---",
		temperature: 0,
		humidity: 0,
		pm25: [0],
		tvoc: [0.0],
		hcho: [0.00]
	})

	const datalinechart = reactive({
		date: ["1999-1-1", "1999-1-2", "1999-1-3", "1999-1-4"],
		pm25: [70, 70, 70, 70],
		tvoc: [0.6, 0.6, 0.6, 0.6],
		hcho: [0.1, 0.1, 0.1, 0.1],
		temperature: [20, 20, 20, 20],
		humidity: [40, 40, 40, 40],
	})

	const optionlinechart = (data => {
		return {
			title: {
				text: '历史数据',
				subtext: '*请先请求数据库得到数据'
			},
			tooltip: {
				trigger: 'axis'
			},
			legend: {
				data: ['温度', '湿度', 'MP2.5', '甲醛', 'TVOC']
			},
			grid: {
				left: '3%',
				right: '4%',
				bottom: '3%',
				containLabel: true
			},
			xAxis: {
				type: 'category',
				data: data.date
			},
			yAxis: {
				type: 'value'
			},
			series: [{
					name: '温度',
					type: 'line',
					data: data.temperature
				}, {
					name: '湿度',
					type: 'line',
					data: data.humidity
				}, {
					name: 'MP2.5',
					type: 'line',
					data: data.pm25
				},
				{
					name: '甲醛',
					type: 'line',
					data: data.hcho
				},
				{
					name: 'TVOC',
					type: 'line',
					data: data.tvoc
				},
			],
		}
	});

	export default {
		name: 'equipmenthome',
		setup(props, {
			root
		}) {
			const goBack = (() => {
				root.$router.push({
					path: '/consoleequipment'
				})
			});

			const ononeday = (() => {
				var data = {
					requirement: "ononeday",
					tid: readData('currentequipment')
				}
				request({
					url: "/equipmenthome",
					data: data
				}).then(res => {
					if (res != false) {
						datalinechart.date = res.date
						datalinechart.pm25 = res.pm25
						datalinechart.hcho = res.hcho
						datalinechart.tvoc = res.tvoc
						datalinechart.temperature = res.temperature
						datalinechart.humidity = res.humidity
						const chartDomlinechart = document.getElementById('linechart');
						const myChartlinechart = echarts.init(chartDomlinechart);
						myChartlinechart.setOption(optionlinechart(datalinechart));
					} else {
						root.$message({
							showClose: true,
							message: '获取该设备一天数据失败',
							type: 'warning'
						})
					}
				}, err => {
					root.$message({
						showClose: true,
						message: '请求服务器错误',
						type: 'error'
					})
					console.log("equipmenthome-ononeday")
					console.log(err)
					console.log("equipmenthome-ononeday")
				})
			})

			const ononeweek = (() => {
				var data = {
					requirement: "ononeweek",
					tid: readData('currentequipment')
				}
				request({
					url: "/equipmenthome",
					data: data
				}).then(res => {
					if (res != false) {
						datalinechart.date = res.date
						datalinechart.pm25 = res.pm25
						datalinechart.hcho = res.hcho
						datalinechart.tvoc = res.tvoc
						datalinechart.temperature = res.temperature
						datalinechart.humidity = res.humidity
						const chartDomlinechart = document.getElementById('linechart');
						const myChartlinechart = echarts.init(chartDomlinechart);
						myChartlinechart.setOption(optionlinechart(datalinechart));
					} else {
						root.$message({
							showClose: true,
							message: '获取该设备一周数据失败',
							type: 'warning'
						})
					}
				}, err => {
					root.$message({
						showClose: true,
						message: '请求服务器错误',
						type: 'error'
					})
					console.log("equipmenthome-ononeweek")
					console.log(err)
					console.log("equipmenthome-ononeweek")
				})
			})

			const ononemonth = (() => {
				var data = {
					requirement: "ononemonth",
					tid: readData('currentequipment')
				}
				request({
					url: "/equipmenthome",
					data: data
				}).then(res => {
					if (res != false) {
						datalinechart.date = res.date
						datalinechart.pm25 = res.pm25
						datalinechart.hcho = res.hcho
						datalinechart.tvoc = res.tvoc
						datalinechart.temperature = res.temperature
						datalinechart.humidity = res.humidity
						const chartDomlinechart = document.getElementById('linechart');
						const myChartlinechart = echarts.init(chartDomlinechart);
						myChartlinechart.setOption(optionlinechart(datalinechart));
					} else {
						root.$message({
							showClose: true,
							message: '获取该设备一月数据失败',
							type: 'warning'
						})
					}
				}, err => {
					root.$message({
						showClose: true,
						message: '请求服务器错误',
						type: 'error'
					})
					console.log("equipmenthome-ononeweek")
					console.log(err)
					console.log("equipmenthome-ononeweek")
				})
			})

			return {
				data,
				goBack,
				ononeday,
				ononeweek,
				ononemonth,
				getequipment: readData('currentequipment'),
			}
		},

		mounted() {
			const option = ((shuju, data) => {
				return {
					title: {
						text: (shuju == "HCHO" ? '甲醛' : shuju) + "浓度",
						subtext: shuju == "PM2.5" ? '单位：μg/m³' : '单位：mg/m³'
					},
					grid: {
						top: '80% '
					},
					xAxis: {
						type: 'value',
						min: 0,
						max: shuju == "PM2.5" ? 250 : 1,
						axisLine: {
							show: false
						},
						splitLine: {
							show: false
						},
					},
					yAxis: {
						type: 'category',
						axisLine: {
							show: false
						},
					},
					series: [{
							//渐变数据内容
							type: 'bar',
							barWidth: 30,
							itemStyle: {
								normal: {
									color: {
										colorStops: [{
											offset: 0,
											color: '#15a675'
										}, {
											offset: 1,
											color: '#ffd127'
										}]
									}
								},
							},
							data: data,
							z: 0
						},
						{
							//辅助分割图形
							type: 'pictorialBar',
							barWidth: 30,
							symbol: 'rect',
							symbolMargin: '100%', //控制分割图形的大小
							symbolSize: [5, '100%'],
							symbolRepeat: true,
							animation: false,
							itemStyle: {
								normal: {
									color: '#ffffff',
								},
							},
							data: data,
							label: {
								show: true,
								position: 'right'
							},
							z: 1
						}
					]
				}
			});

			const chartDom = document.getElementById('pm25');
			const myChart = echarts.init(chartDom);
			myChart.setOption(option("PM2.5", data.pm25));

			const chartDom1 = document.getElementById('hcho');
			const myChart1 = echarts.init(chartDom1);
			myChart1.setOption(option("HCHO", data.hcho));

			const chartDom2 = document.getElementById('tvoc');
			const myChart2 = echarts.init(chartDom2);
			myChart2.setOption(option("TVOC", data.tvoc));

			this.timer = setInterval(() => {
				console.log("开始")
				var data = {
					requirement: "onquery",
					tid: readData('currentequipment')
				}
				request({
					url: "/equipmenthome",
					data: data
				}).then(res => {
					if (res != false) {
						this.data.date = res.date
						this.data.temperature = res.temperature
						this.data.humidity = res.humidity
						this.data.address = res.address
						myChart.setOption(option("PM2.5", [res.pm25]));
						myChart1.setOption(option("HCHO", [res.hcho]));
						myChart2.setOption(option("TVOC", [res.tvoc]));
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
					console.log("equipmenthome-onquery")
					console.log(err)
					console.log("equipmenthome-onquery")
				})
			}, 10000)
		},

		beforeDestroy() {
			if (this.timer) {
				clearInterval(this.timer); //关闭
			} //利用vue的生命周期函数
		}
	}
</script>

<style lang="scss" scoped>
	#equipment-style {
		position: absolute;
		top: 20px;
		left: 20px;
		right: 20px;
		bottom: 20px;
		box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)
	}

	.el-style {
		margin-left: 10px;
		margin-right: 10px;
		line-height: 50px;
	}

	.el-button-style {
		margin: auto;
	}

	.label-style {
		line-height: 50px;
		font-size: 20px;
		color: blue;
	}

	.div-style {
		border-radius: 20px;
		height: 40px;
		line-height: 40px;
		background-color: #424242;
		color: white;
	}

	.div-style1 {
		position: relative;
		width: 25%;
		margin-top: 30px;
		margin-left: 75%;
		z-index: 2
	}

	.div-style2 {
		position: relative;
		margin-top: -30px;
		margin-left: 10px;
		margin-right: 10px;
		z-index: 1
	}

	.el-col-style {
		box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04)
	}

	.el-col-width-style {
		width: 15px;
	}

	.h5-style1 {
		line-height: 25px;
	}

	.h4-style1 {
		margin-left: 5px;
	}
</style>
