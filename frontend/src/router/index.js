import { createRouter, createWebHistory } from 'vue-router';
import AutoParts from '../components/AutoParts.vue';
import Customers from '../components/Customers.vue';
import Home from '../components/Home.vue';
import Billing from '../components/Billing.vue';
import Bills from '../components/Bills.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/storage',
      name: 'AutoParts',
      component: AutoParts,
    },
    {
      path: '/customers',
      name: 'Customers',
      component: Customers,
      props: (route) => ({
        successful: route.query.successful
      })
    },
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      path: '/billing',
      name: 'Billing',
      component: Billing,
      props: (route) => ({
        paramId: route.query.paramId,
        paramName: route.query.paramName,
        paramTaxNumber: route.query.paramTaxNumber,
        paramPostalCode: route.query.paramPostalCode,
        paramSettlement: route.query.paramSettlement,
        paramAddress: route.query.paramAddress,
      }),
    },
    {
      path: '/bills',
      name: 'Bills',
      component: Bills,
    }
  ]
})

export default router
