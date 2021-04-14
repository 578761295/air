<template>
	<div id="nav-style">
		<el-menu :collapse="isCollapse" background-color="transparent" text-color="#fff" router>
			<template v-for="(item, index) in routers">
				<el-submenu v-if="!item.hidden" :key="item.id" :index="index + ''">
					<template slot="title">
						<i :class="item.meta.icon"></i>
						<span slot="title">{{ item.meta.name }}</span>
					</template>
					<el-menu-item v-for="subItem in item.children" :key="subItem.id" :index="subItem.path">{{ subItem.meta.name }}</el-menu-item>
				</el-submenu>
			</template>
		</el-menu>
	</div>
</template>

<script>
	import {
		reactive,
		ref
	} from '@vue/composition-api'
	export default {
		name: 'navMenu',
		setup(props, {
			root
		}) {
			// 控制菜单展开收起
			const isCollapse = ref(false)
			// 获取菜单变量
			const routers = reactive(root.$router.options.routes)

			return {
				isCollapse,
				routers
			}
		}
	}
</script>

<style lang="scss" scoped>
	#nav-style {
		position: absolute;
		top: 50px;
		bottom: 0px;
		width: 200px;
		background-color: #B3D8FF;
		-webkit-box-shadow: 0 3px 16px 0 rgba(0, 0, 0, .1);
	}
</style>
