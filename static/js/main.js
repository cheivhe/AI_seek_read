// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 添加平滑滚动效果
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
    
    // 为文章卡片添加点击效果
    const articleCards = document.querySelectorAll('.article-card');
    articleCards.forEach(card => {
        card.addEventListener('click', function(e) {
            // 如果点击的不是链接本身，则模拟点击卡片内的第一个链接
            if (!e.target.closest('a')) {
                const link = this.querySelector('a');
                if (link) {
                    window.open(link.href, '_blank');
                }
            }
        });
    });
    
    // 处理刷新按钮点击
    const refreshButton = document.getElementById('refresh-button');
    if (refreshButton) {
        refreshButton.addEventListener('click', function() {
            const mainContent = document.querySelector('main');
            mainContent.classList.add('loading');
            
            // 延迟一下再跳转，以便显示加载动画
            setTimeout(function() {
                window.location.href = refreshButton.getAttribute('href');
            }, 500);
            
            return false;
        });
    }
    
    // 创建滚动到顶部按钮
    const scrollTopButton = document.createElement('div');
    scrollTopButton.className = 'scroll-top';
    scrollTopButton.innerHTML = '↑';
    document.body.appendChild(scrollTopButton);
    
    // 滚动到顶部功能
    scrollTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // 监听滚动事件，控制按钮显示
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollTopButton.classList.add('visible');
        } else {
            scrollTopButton.classList.remove('visible');
        }
    });
    
    // 添加页面淡入效果
    document.querySelector('main').classList.add('fade-in');
    
    // 为文章内容中的图片添加点击放大效果
    document.querySelectorAll('.article-content img').forEach(img => {
        img.addEventListener('click', function() {
            this.classList.toggle('expanded');
        });
    });
});