<template>
	<!-- 必须有一层父元素 -->
	<div id="app">
		<!-- 内容区 -->
		<router-view />
	</div>
</template>

<script>
	export default {
		name: 'App',
		setup() {
		},
	}
</script>

<style>
	* {
		padding: 0;
		margin: 0;
	}
</style>

<!--
<Script>样式
Name:当前的名字
Components:组件，有引入组件时，放入组件名称
Data:数据，V-model绑定数据使用
Created:创建完成时（生命周期其中之一）
Mounted:挂载完成时（生命周期之一）
Methods:定义函数
Props、Watch:子组件接收父组件参数

<style>样式
Lang="scss":定义类型
Scoped:局部。定义是，只有当前文件应用该样式。
-->
