<template>
	<div>
		<el-button type="primary" class="bt-warp" icon="el-icon-menu" @click="Openconsole()">管理台</el-button>
		<baidu-map class="map" :center="center" :zoom="zoom" @ready="handler" :scroll-wheel-zoom="true">
			<bm-geolocation anchor="BMAP_ANCHOR_BOTTOM_RIGHT" :showAddressBar="true" :autoLocation="true"></bm-geolocation>
		</baidu-map>
	</div>
</template>

<script>
	import {
		readData
	} from "../../utils/storageUtils.js"
	import {
		request
	} from "../../utils/request.js"
	var markpoint = []
	export default {
		setup(props, {
			root
		}) {
			const Openconsole = (() => {
				root.$router.push({
					path: '/console'
				})
			})

			const getPoints = (({
				BMap,
				map
			}, position) => {
				var that = this
				var point = new BMap.Point(position.lng, position.lat)
				var marker = new BMap.Marker(point)
				map.addOverlay(marker)
				var content = "<table>";
				content = content + "<tr><td> 设备地点：" + position.address + " </td></tr>";
				content = content + "<tr><td> 设备id：" + position.tid + " </td></tr>";
				content = content + "<tr><td> 时间：" + position.finalresponsetime + "</td></tr>";
				content += "</table>";
				// 设置提示框的内容
				var infoWindow = new BMap.InfoWindow(content)
				marker.addEventListener('click', function() {
					map.openInfoWindow(infoWindow, point)
				})
			})

			const handler = (({
				BMap,
				map
			}) => {
				var data = {
					mailbox: readData('currentuser')
				}
				request({
					url: "/equipmentmap",
					data: data
				}).then(res => {
					if (res != false) {
						markpoint = res
						// 将标记点 渲染
						markpoint.forEach((item) => {
							getPoints({
									BMap,
									map,
								},
								item)
						})
						map.enableScrollWheelZoom(true)
					} else {
						this.$message({
							showClose: true,
							message: '获取用户设备点失败',
							type: 'error'
						})
					}
				}, err => {
					this.$message({
						showClose: true,
						message: '请求服务器错误',
						type: 'error'
					})
					console.log("equipmentmap")
					console.log(err)
					console.log("equipmentmap")
				})
			})

			return {
				handler,
				Openconsole,
				center: {
					lng: 110,
					lat: 22
				},
				zoom: 10,
				//标记点
				markpoint: markpoint
			}
		},
		methods: {
			// 关闭信息窗口 @close 自带的方法
			infoWindowClose(marker) {
				this.markpoint[marker].showFlag = false
			},

			// 打开信息框
			infoWindowOpen(marker) {
				this.markpoint[marker].showFlag = true
			}
		},
	}
</script>

<style lang="scss" scoped>
	.map {
		position: absolute;
		width: 100%;
		height: 100%;
		margin-top: -49px;
		z-index: 1
	}

	.bt-warp {
		position: relative;
		margin-top: 20px;
		margin-left: 90%;
		margin-bottom: -50px;
		z-index: 2
	}
</style>


<!-- 
<template>
	<div>
		<el-button type="primary" class="bt-warp" icon="el-icon-menu" @click="Openconsole()">管理台</el-button>
		<baidu-map class="map" :center="center" :zoom="zoom" @ready="handler" :scroll-wheel-zoom="true">
			<bm-geolocation anchor="BMAP_ANCHOR_BOTTOM_RIGHT" :showAddressBar="true" :autoLocation="true"></bm-geolocation>
		</baidu-map>
	</div>
</template>

<script>
	import {
		readData
	} from "../../utils/storageUtils.js"
	import {
		request
	} from "../../utils/request.js"
	const markpoint = []
	export default {
		setup(props, {
			root
		}) {
			const Openconsole = (() => {
				root.$router.push({
					path: '/console'
				})
			})
			return {
				Openconsole,
				center: {
					lng: 110,
					lat: 22
				},
				zoom: 8,
				//标记点
				markpoint: markpoint
			}
		},
		beforeCreate() {
			var data = {
				mailbox: readData('currentuser')
			}
			request({
				url: "/equipmentmap",
				data: data
			}).then(res => {
				if (res != false) {
					this.markpoint = res
					console.log("start")
				} else {
					this.$message({
						showClose: true,
						message: '获取用户设备点失败',
						type: 'error'
					})
				}
			}, err => {
				this.$message({
					showClose: true,
					message: '请求服务器错误',
					type: 'error'
				})
				console.log("equipmentmap")
				console.log(err)
				console.log("equipmentmap")
			})
		},
		methods: {
			handler({
				BMap,
				map
			}) {
				console.log(1)
				// 将标记点 渲染
				this.markpoint.forEach((item) => {
					console.log("item")
					console.log(item)
					console.log("item")
					this.getPoints({
							BMap,
							map,
						},
						item)
				})
				map.enableScrollWheelZoom(true)
			},

			getPoints({
				BMap,
				map
			}, position) {
				console.log(position)
				var that = this
				var point = new BMap.Point(position.lng, position.lat)
				var marker = new BMap.Marker(point)
				map.addOverlay(marker)
				var content = "<table>";
				content = content + "<tr><td> 设备地点：" + position.name + " </td></tr>";
				content = content + "<tr><td> 设备id：" + position.tid + " </td></tr>";
				content = content + "<tr><td> 时间：2018-1-3</td></tr>";
				content += "</table>";
				// 设置提示框的内容
				var infoWindow = new BMap.InfoWindow(content)
				marker.addEventListener('click', function() {
					map.openInfoWindow(infoWindow, point)
				})
			},

			// 关闭信息窗口 @close 自带的方法
			infoWindowClose(marker) {
				this.markpoint[marker].showFlag = false
			},

			// 打开信息框
			infoWindowOpen(marker) {
				this.markpoint[marker].showFlag = true
			}
		},
	}
</script>

<style lang="scss" scoped>
	.map {
		position: absolute;
		width: 100%;
		height: 100%;
		margin-top: -49px;
		z-index: 1
	}

	.bt-warp {
		position: relative;
		margin-top: 20px;
		margin-left: 90%;
		margin-bottom: -50px;
		z-index: 2
	}
</style>


<!-- <template>
	<div>
		<el-button type="primary" class="bt-warp" icon="el-icon-menu" @click="Openconsole()">管理台</el-button>
		<baidu-map class="map" :center="center" :zoom="zoom" @ready="handler" :scroll-wheel-zoom="true">
			<bm-geolocation anchor="BMAP_ANCHOR_BOTTOM_RIGHT" :showAddressBar="true" :autoLocation="true"></bm-geolocation>
		</baidu-map>
	</div>
</template>

<script>
	import {
		readData
	} from "../../utils/storageUtils.js"
	import {
		request
	} from "../../utils/request.js"
	const markpoint = []
	export default {
		data(root) {
			const Openconsole = (() => {
				root.$router.push({
					path: '/console'
				})
			})
			return {
				Openconsole,
				center: {
					lng: 0,
					lat: 0
				},
				zoom: 3,
				//标记点
				markpoint: markpoint
			}
		},
		created() {
			var data = {
				mailbox: readData('currentuser')
			}
			request({
				url: "/equipmentmap",
				data: data
			}).then(res => {
				if (res != false) {
					console.log("start")
					this.markpoint = res
					console.log(this.markpoint)
					console.log("start")
				} else {
					root.$message({
						showClose: true,
						message: '获取用户设备点失败',
						type: 'error'
					})
				}
			}, err => {
				root.$message({
					showClose: true,
					message: '请求服务器错误',
					type: 'error'
				})
				console.log("equipmentmap")
				console.log(err)
				console.log("equipmentmap")
			})
		},
		methods: {
			handler({
				BMap,
				map
			}) {
				this.center.lng = 110
				this.center.lat = 22
				this.zoom = 8
				// 将标记点 渲染
				this.markpoint.forEach((item) => {
					this.getPoints({
						BMap,
						map
					}, item)
				})
				map.enableScrollWheelZoom(true)
			},
			getPoints({
				BMap,
				map
			}, position) {
				var that = this
				var point = new BMap.Point(position.lng, position.lat)
				var marker = new BMap.Marker(point)
				map.addOverlay(marker)
				var content = "<table>";
				content = content + "<tr><td> 设备地点：" + position.name + " </td></tr>";
				content = content + "<tr><td> 时间：2018-1-3</td></tr>";
				content += "</table>";
				// 设置提示框的内容
				var infoWindow = new BMap.InfoWindow(content)
				marker.addEventListener('click', function() {
					map.openInfoWindow(infoWindow, point)
				})
			},
			// 关闭信息窗口 @close 自带的方法
			infoWindowClose(marker) {
				this.markpoint[marker].showFlag = false
			},
			// 打开信息框
			infoWindowOpen(marker) {
				this.markpoint[marker].showFlag = true
			}
		},
	}
</script>

<style lang="scss" scoped>
	.map {
		position: absolute;
		width: 100%;
		height: 100%;
		margin-top: -49px;
		z-index: 1
	}

	.bt-warp {
		position: relative;
		margin-top: 20px;
		margin-left: 90%;
		margin-bottom: -50px;
		z-index: 2
	}
</style>
 -->

 -->
