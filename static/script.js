function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('collapsed');
}

// 检测屏幕宽度并在窄屏时调整导航栏内容
function adjustNavbarForMobile() {
    const navbar = document.querySelector('.navbar');
    const windowWidth = window.innerWidth;
    
    if (windowWidth <= 768) {
        // 窄屏时：替换标题为"4C的学习资料"，只保留4C01，移除其他链接
        const titleElement = navbar.querySelector('h1');
        if (titleElement) {
            titleElement.textContent = '4C的学习资料';
        }
        
        // 隐藏Trystage和项目画廊链接，只保留4C01
        const navLinks = navbar.querySelector('.nav-links');
        if (navLinks) {
            // 移除所有desktop-only类的元素
            const desktopLinks = navLinks.querySelectorAll('.desktop-only');
            desktopLinks.forEach(link => {
                link.style.display = 'none';
            });
        }
    } else {
        // 宽屏时：恢复原始标题和导航链接
        const titleElement = navbar.querySelector('h1');
        if (titleElement) {
            titleElement.textContent = '4C01的学习资料';
        }
    }
}

// 检查屏幕宽度，如果窄则默认收起侧边栏
function checkScreenSize() {
    const sidebar = document.querySelector('.sidebar');
    if (window.innerWidth <= 768) {
        // 如果屏幕宽度小于等于768px，则收起侧边栏
        sidebar.classList.add('collapsed');
    } else {
        // 否则展开侧边栏
        sidebar.classList.remove('collapsed');
    }
}

// 页面加载完成后调整导航栏和检查屏幕尺寸
document.addEventListener('DOMContentLoaded', function() {
    adjustNavbarForMobile();
    checkScreenSize();
});

// 监听窗口大小变化
window.addEventListener('resize', function() {
    adjustNavbarForMobile();
    checkScreenSize();
});