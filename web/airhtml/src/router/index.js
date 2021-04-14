import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const routes = [{
		path: "/",
		// 路由重定向
		redirect: "login",
		// redirect: "console",
		hidden: true,
		meta: {
			name: "首页"
		}
	},
	{
		path: "/login",
		name: "login",
		hidden: true,
		meta: {
			name: "登录"
		},
		component: () =>
			import("../views/login/Login.vue")
	},
	{
		path: "/console",
		name: "console",
		meta: {
			name: "控制台",
			icon: "el-icon-menu"
		},
		redirect: "consoleequipment",
		component: () =>
			import("../views/layout/Layout.vue"),
		// 多重菜单自定义方式
		children: [{
			path: "/consoleequipment",
			name: "consoleequipment",
			meta: {
				name: "设备"
			},
			component: () =>
				import("../views/console/Consoleequipment.vue")
		}, ]
	},
	{
		path: "/equipmenthome",
		name: "equipmenthome",
		hidden: true,
		meta: {
			name: "设备主页",
		},
		redirect: "equipmenthome",
		component: () =>
			import("../views/layout/Layout.vue"),
		// 多重菜单自定义方式
		children: [{
			// 概览
			path: "/equipmenthome",
			name: "equipmenthome",
			meta: {
				name: "设备详情"
			},
			component: () =>
				import("../views/equipment/Equipmenthome.vue")
		}, ]
	},
	{
		path: "/useradministrator",
		name: "useradministrator",
		hidden: true,
		meta: {
			name: "用户管理员模式",
		},
		redirect: "useradministrator",
		component: () =>
			import("../views/layout/Layout.vue"),
		// 多重菜单自定义方式
		children: [{
			// 概览
			path: "/useradministrator",
			name: "useradministrator",
			meta: {
				name: "用户管理员"
			},
			component: () =>
				import("../views/administrator/Useradministrator.vue")
		}, ]
	},
	{
		path: "/superadministrator",
		name: "superadministrator",
		hidden: true,
		meta: {
			name: "超级管理员模式",
		},
		redirect: "superadministrator",
		component: () =>
			import("../views/layout/Layout.vue"),
		// 多重菜单自定义方式
		children: [{
			// 概览
			path: "/superadministrator",
			name: "superadministrator",
			meta: {
				name: "超级管理员"
			},
			component: () =>
				import("../views/administrator/Superadministrator.vue")
		}, ]
	},
	{
		path: "/consolepersonal",
		name: "consolepersonal",
		meta: {
			name: "个人中心",
			icon: "el-icon-s-custom"
		},
		redirect: "consolepersonal",
		component: () =>
			import("../views/layout/Layout.vue"),
		// 多重菜单自定义方式
		children: [{
			// 概览
			path: "/consolepersonal",
			name: "consolepersonal",
			meta: {
				name: "账户设置"
			},
			component: () =>
				import("../views/console/Consolepersonal.vue")
		}, ]
	},
	{
		path: "/equipmentmap",
		name: "equipmentmap",
		hidden: true,
		component: () =>
			import("../views/map/Equipmentmap.vue")
	},
];

const router = new VueRouter({
	mode: "history",
	base: process.env.BASE_URL,
	routes
});

export default router;
