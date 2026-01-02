/**
 * 电商运营数据分析知识网页 - JavaScript
 * 包含：移动端菜单、平滑滚动等基础功能
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // ========================================
    // 侧边栏平台展开/折叠
    // ========================================
    const platformLinks = document.querySelectorAll('.platform-link');
    
    platformLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const platformGroup = this.closest('.platform-group');
            const isActive = platformGroup.classList.contains('active');
            
            // 关闭其他平台
            document.querySelectorAll('.platform-group').forEach(group => {
                if (group !== platformGroup) {
                    group.classList.remove('active');
                }
            });
            
            // 切换当前平台
            platformGroup.classList.toggle('active', !isActive);
            
            // 如果是跳转链接，延迟跳转
            const href = this.getAttribute('href');
            if (href && !isActive) {
                setTimeout(() => {
                    window.location.href = href;
                }, 300);
            }
        });
    });
    
    // ========================================
    // 移动端侧边栏切换
    // ========================================
    const navToggle = document.querySelector('.nav-toggle');
    const sidebar = document.querySelector('.sidebar');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (navToggle && sidebar) {
        navToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
            if (mobileMenu) {
                mobileMenu.classList.toggle('active');
            }
        });
    }
    
    // ========================================
    // 移动端菜单切换（保留原有功能）
    // ========================================
    if (navToggle && mobileMenu) {
        // 点击菜单项后关闭菜单
        const mobileLinks = mobileMenu.querySelectorAll('.mobile-link');
        mobileLinks.forEach(link => {
            link.addEventListener('click', function() {
                mobileMenu.classList.remove('active');
                if (sidebar) sidebar.classList.remove('active');
                if (navToggle) navToggle.classList.remove('active');
            });
        });
        
        // 点击页面其他区域关闭菜单
        document.addEventListener('click', function(e) {
            if (navToggle && !navToggle.contains(e.target) && 
                mobileMenu && !mobileMenu.contains(e.target) &&
                sidebar && !sidebar.contains(e.target)) {
                mobileMenu.classList.remove('active');
                if (sidebar) sidebar.classList.remove('active');
                if (navToggle) navToggle.classList.remove('active');
            }
        });
    }
    
    // ========================================
    // 平滑滚动到锚点
    // ========================================
    const formulaNavLinks = document.querySelectorAll('.formula-nav-link');
    
    formulaNavLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                const navHeight = document.querySelector('.formula-nav').offsetHeight + 80;
                const targetPosition = targetElement.offsetTop - navHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                // 高亮目标卡片
                targetElement.classList.add('highlight');
                setTimeout(() => {
                    targetElement.classList.remove('highlight');
                }, 1500);
            }
        });
    });
    
    // ========================================
    // 滚动时高亮当前公式导航
    // ========================================
    function updateActiveNavLink() {
        const formulaCards = document.querySelectorAll('.formula-card');
        const navLinks = document.querySelectorAll('.formula-nav-link');
        
        if (formulaCards.length === 0 || navLinks.length === 0) return;
        
        let currentId = '';
        const scrollPosition = window.scrollY + 200;
        
        formulaCards.forEach(card => {
            const cardTop = card.offsetTop;
            if (scrollPosition >= cardTop) {
                currentId = card.id;
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + currentId) {
                link.classList.add('active');
            }
        });
    }
    
    window.addEventListener('scroll', updateActiveNavLink);
    
    // ========================================
    // 分类卡片悬停效果（首页）
    // ========================================
    const categoryCards = document.querySelectorAll('.category-card');
    
    categoryCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.setProperty('--hover-scale', '1.02');
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.setProperty('--hover-scale', '1');
        });
    });
    
    // ========================================
    // 数字输入框增强
    // ========================================
    const numberInputs = document.querySelectorAll('.calc-input[type="number"]');
    
    numberInputs.forEach(input => {
        // 阻止滚轮改变数值
        input.addEventListener('wheel', function(e) {
            e.preventDefault();
        });
        
        // 选中时全选内容
        input.addEventListener('focus', function() {
            this.select();
        });
    });
    
    // ========================================
    // 添加输入提示动画
    // ========================================
    const inputGroups = document.querySelectorAll('.input-group');
    
    inputGroups.forEach((group, index) => {
        group.style.animationDelay = `${index * 0.1}s`;
    });
    
    // ========================================
    // 页面加载动画
    // ========================================
    function animateOnScroll() {
        const elements = document.querySelectorAll('.category-card, .preview-card, .formula-card');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
        
        elements.forEach(el => {
            el.classList.add('animate-on-scroll');
            observer.observe(el);
        });
    }
    
    // 添加动画样式
    const style = document.createElement('style');
    style.textContent = `
        .animate-on-scroll {
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.5s ease, transform 0.5s ease;
        }
        .animate-on-scroll.visible {
            opacity: 1;
            transform: translateY(0);
        }
        .formula-card.highlight {
            box-shadow: 0 0 0 3px var(--accent-color), var(--shadow-lg);
        }
        .formula-nav-link.active {
            background: var(--primary-color);
            color: white;
        }
    `;
    document.head.appendChild(style);
    
    animateOnScroll();
    
    // ========================================
    // 键盘导航支持
    // ========================================
    document.addEventListener('keydown', function(e) {
        // ESC 键关闭移动菜单
        if (e.key === 'Escape' && mobileMenu) {
            mobileMenu.classList.remove('active');
            if (navToggle) navToggle.classList.remove('active');
        }
    });
    
    // ========================================
    // 工具函数：格式化数字
    // ========================================
    window.formatNumber = function(num, decimals = 2) {
        if (isNaN(num) || !isFinite(num)) return '--';
        
        if (Math.abs(num) >= 10000) {
            return num.toLocaleString('zh-CN', {
                maximumFractionDigits: decimals
            });
        }
        return num.toFixed(decimals);
    };
    
    // ========================================
    // 工具函数：复制到剪贴板
    // ========================================
    window.copyToClipboard = function(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                showToast('已复制到剪贴板');
            }).catch(() => {
                fallbackCopy(text);
            });
        } else {
            fallbackCopy(text);
        }
    };
    
    function fallbackCopy(text) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        try {
            document.execCommand('copy');
            showToast('已复制到剪贴板');
        } catch (err) {
            showToast('复制失败');
        }
        document.body.removeChild(textarea);
    }
    
    // ========================================
    // 工具函数：显示提示消息
    // ========================================
    window.showToast = function(message, duration = 2000) {
        const existing = document.querySelector('.toast-message');
        if (existing) existing.remove();
        
        const toast = document.createElement('div');
        toast.className = 'toast-message';
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: var(--bg-dark);
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 14px;
            z-index: 1000;
            animation: fadeInUp 0.3s ease;
        `;
        
        const animation = document.createElement('style');
        animation.textContent = `
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateX(-50%) translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateX(-50%) translateY(0);
                }
            }
        `;
        document.head.appendChild(animation);
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transition = 'opacity 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    };
    
    console.log('📊 电商运营数据分析知识网页已加载');
});

