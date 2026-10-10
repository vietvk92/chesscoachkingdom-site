#!/usr/bin/env python3
"""Generates the static Chess Coach Kingdom site. Run `python3 tools/build_site.py` from anywhere (assets: tools/build_assets.py).
Privacy page bodies are taken verbatim from the previous version of the pages (git HEAD) so the legal text is unchanged."""
import os, re, subprocess, html

SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..') + '/'
APP_STORE_URL = ''  # TODO owner: paste the App Store URL here (https://apps.apple.com/app/id...). Empty = non-link text.
APP_ID = ''         # TODO owner: numeric App Store id, enables the apple-itunes-app smart banner below.
EMAIL = 'support@chesscoachkingdom.com'
ORIGIN = 'https://chesscoachkingdom.com'
EULA = 'https://www.apple.com/legal/internet-services/itunes/dev/stdeula/'

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600&family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&display=swap">')


def pic(src, alt, w, h, cls='', lazy=True, ext='jpg', sizes=None, fetch=False):
    """<picture> with webp + fallback."""
    a = f' class="{cls}"' if cls else ''
    ld = ' loading="lazy" decoding="async"' if lazy else (' fetchpriority="high"' if fetch else '')
    return (f'<picture><source type="image/webp" srcset="/assets/{src}.webp">'
            f'<img{a} src="/assets/{src}.{ext}" alt="{html.escape(alt)}" width="{w}" height="{h}"{ld}></picture>')


# ----------------------------------------------------------------------------------------------- copy
EN = dict(
    lang='en', home='/', alt_lang=('vi', '/vi/', 'Tiếng Việt'),
    title='Chess Coach Kingdom — Learn chess as an adventure',
    desc='Journey through a chess kingdom with Firefly, your lantern-carrying guide: bite-size lessons, puzzles for your level, daily rival challenges and an on-device coach.',
    nav=[('#kingdom', 'The kingdom'), ('#firefly', 'Firefly'), ('#train', 'Train'), ('#private', 'Private'), ('#plus', 'Plus')],
    support='/support/', privacy='/privacy/en/', support_l='Support', privacy_l='Privacy Policy', terms_l='Terms of Use',
    eyebrow='A chess companion for the whole family',
    h1='Learn chess as an <em>adventure</em>',
    lead='Journey through a chess kingdom with Firefly, your lantern-carrying guide: bite-size lessons, puzzles for your level, daily rival challenges and an on-device coach.',
    avail='Available on iPhone &amp; iPad', badge_get='Download on the App Store', pills=['No accounts', 'No ads', 'Works offline'],
    shot='iphone', shotdir='iphone',
    k_eyebrow='The kingdom', k_h='A storybook map of 14 regions',
    k_p='Walk from Pawn Village to the Library of Classic Games. Short interactive lessons, a placement test that starts you at the right spot, gate challenges and a letter in your journal every day. Lessons unlock in order: finish one to open the next.',
    regions=[('village', 'Pawn Village', 'Where every journey begins: cottages shaped like pawns, soft checkerboard fields and little bridges.'),
             ('citadel', 'City of the Pieces', 'A lively town of rook towers, bishop spires and a queen&rsquo;s palace on the hill.'),
             ('fortress', 'Fortress of Rules', 'Banners, a drawbridge and a king&rsquo;s keep above the mist.'),
             ('forest', 'Tactics Forest', 'Lantern-lit paths, stone pieces as statues and forks in the road.')],
    res_h='Friendly residents', res_p='Every region has its own people to meet. They cheer you on, set you challenges and, after a game, will talk it through with you.',
    f_eyebrow='Meet Firefly', f_h='A lantern, a knight, a friend',
    f_p='Firefly, a lantern-carrying knight, greets you each day, cheers your good moves and shows the way when you are stuck. A translucent piece glides along the move to make, so you see the idea instead of just reading it.',
    hint_h='Three gentle levels of hints', hint_p='Ask for a little help or a lot. The lantern only burns as bright as you need.',
    hints=[('A first nudge', 'A gentle hint about which idea to look for.'), ('A closer look', 'Points to the piece or the square that matters.'), ('The move itself', 'Shows the best move, so you can see why it works.')],
    t_eyebrow='Train', t_h='Small steps, every day',
    t_cards=[('Bite-size lessons', 'Short, interactive lessons you can finish in a few minutes, with a three-level lantern hint whenever you get stuck.'),
             ('Puzzles for your level', 'Tactics, checkmate patterns, openings and endgames, picked to match how you play.'),
             ('Daily challenge &amp; more', 'A daily challenge, the Endless Trail and the weekly tournament keep practice fresh.'),
             ('Fix Workshop', 'Mistakes review turns your own errors into practice, so every slip teaches something.')],
    r_eyebrow='Rivals', r_h='Rivals who write back',
    r_p='Five AI personalities, each with a distinct style, send you daily challenge letters. Lose a game and it can come back as a revenge match.',
    rivals=[('kai', 'Kai'), ('luna', 'Luna'), ('milo', 'Milo'), ('nova', 'Nova'), ('orion', 'Orion')],
    c_eyebrow='The coach', c_h='A coach on your device, always by your side',
    c_p='Ask the coach while you play, get hints, and review every game afterwards. After a game, Ask the Resident for a short chat about your mistakes, your best move or what to try next.',
    c_note='Explanations are generated on your device, with Apple Intelligence when available and built-in templates otherwise. The engine always makes the evaluation.',
    p_eyebrow='Private by design', p_h='Everything stays on your device',
    p_p='The engine, the coach, your games and your stats all run on your device. Your games, photos and coach chats never leave it.',
    p_list=[('No accounts', 'Open the app and play.'), ('No ads', 'Never, anywhere in the app.'), ('No tracking', 'No data collection of any kind.'), ('Works offline', 'On a plane or off the grid.')],
    fam_eyebrow='For the whole family', fam_h='Playful for kids, calm for grown-ups',
    kid_h='Kids mode', kid_p='Firefly cheers every good move and pieces react subtly on the board. Warm, playful and encouraging.',
    adult_h='Adult mode', adult_p='A calmer, stats-first experience, with the same coach and the same lessons.',
    fam_list=[('One profile per player', 'Each player gets a profile on the same device with their own progress, badges and journal. Adding, renaming or deleting profiles sits behind a parental gate.'),
              ('Parent Corner', 'Play-time reports for parents.'),
              ('Made to be accessible', 'VoiceOver, Dynamic Type and Reduce Motion support.'),
              ('Six interface languages', 'Vietnamese, English, Spanish, Portuguese (Brazil), German and French. Lessons are in Vietnamese and English.')],
    g_eyebrow='In the app', g_h='A look around the kingdom', g_prev='Previous screenshots', g_next='Next screenshots',
    cap=dict(home='Home', learn='The kingdom map', coach='Coach', review='Game review', scan='Scan a real board', family='Family', festival='Festivals', resident='Ask the Resident', training='Training', game='Play'),
    plus_eyebrow='Chess Coach Plus', plus_h='Free to start, Plus when you want more',
    plus_free_h='Free', plus_free=['Playing the game', 'The basics lessons', 'Daily practice'],
    plus_h2='Plus', plus_list=['Unlimited puzzles and mistakes practice', 'Full game analysis', 'Unlimited coach hints', 'Every lesson: Openings, Tactics, Endgames', 'The Black opening repertoire', 'All Endgame Yard templates', 'Resident tier challenges', 'Premium board themes and piece sets'],
    plus_p='Choose monthly, yearly (with a free trial) or a one-time lifetime purchase. All three support Family Sharing. Pricing is shown in the app in your local currency.',
    plus_legal='Subscriptions renew automatically until you cancel in your Apple Account settings; payment is charged to your Apple Account.',
    cta_h='Your kingdom is waiting', cta_p='Bring a lantern.',
    foot_tag='Learn chess as an adventure',
)

VI = dict(
    lang='vi', home='/vi/', alt_lang=('en', '/', 'English'),
    title='Chess Coach Kingdom — Học cờ vua như một cuộc phiêu lưu',
    desc='Du hành qua vương quốc cờ vua cùng Firefly, hiệp sĩ cầm đèn: bài học ngắn, câu đố đúng trình độ, thử thách hằng ngày từ các đối thủ và huấn luyện viên chạy ngay trên thiết bị.',
    nav=[('#kingdom', 'Vương quốc'), ('#firefly', 'Firefly'), ('#train', 'Luyện tập'), ('#private', 'Riêng tư'), ('#plus', 'Plus')],
    support='/support/vi/', privacy='/privacy/vi/', support_l='Hỗ trợ', privacy_l='Chính sách quyền riêng tư', terms_l='Điều khoản sử dụng',
    eyebrow='Người bạn đồng hành cờ vua cho cả gia đình',
    h1='Học cờ vua như một <em>cuộc phiêu lưu</em>',
    lead='Du hành qua vương quốc cờ vua cùng Firefly, hiệp sĩ cầm đèn: bài học ngắn, câu đố đúng trình độ, thử thách hằng ngày từ các đối thủ và huấn luyện viên chạy ngay trên thiết bị.',
    avail='Có trên iPhone &amp; iPad', badge_get='Tải trên App Store', pills=['Không tài khoản', 'Không quảng cáo', 'Chơi được khi offline'],
    shot='iphone-vi', shotdir='iphone_vi',
    k_eyebrow='Vương quốc', k_h='Bản đồ cổ tích với 14 vùng đất',
    k_p='Đi từ Làng Tốt đến Thư viện Ván cờ Kinh điển. Bài học tương tác ngắn, bài kiểm tra xếp lớp để bạn bắt đầu đúng chỗ, thử thách cổng và một lá thư trong nhật ký mỗi ngày. Bài học mở khóa theo thứ tự: xong bài này mới mở bài sau.',
    regions=[('village', 'Làng Tốt', 'Nơi mọi hành trình bắt đầu: nhà tranh hình quân tốt, cánh đồng ô bàn cờ và những cây cầu nhỏ.'),
             ('citadel', 'Thành Quân Cờ', 'Thị trấn nhộn nhịp với tháp xe, chóp tượng và cung điện của hậu trên đồi.'),
             ('fortress', 'Pháo đài Luật Lệ', 'Cờ hiệu, cầu kéo và tòa thành của vua trên làn sương mỏng.'),
             ('forest', 'Rừng Chiến Thuật', 'Lối đi thắp đèn lồng, tượng quân cờ bằng đá và những ngã ba đường.')],
    res_h='Những cư dân thân thiện', res_p='Mỗi vùng đất có những người riêng để làm quen. Họ cổ vũ bạn, giao thử thách và sau mỗi ván sẽ cùng bạn nhìn lại.',
    f_eyebrow='Gặp Firefly', f_h='Một chiếc đèn, một hiệp sĩ, một người bạn',
    f_p='Firefly, hiệp sĩ cầm đèn, chào bạn mỗi ngày, cổ vũ những nước đi hay và chỉ đường khi bạn bí. Một quân cờ mờ trượt theo nước cần đi, để bạn thấy ý tưởng thay vì chỉ đọc chữ.',
    hint_h='Ba mức gợi ý nhẹ nhàng', hint_p='Cần giúp ít hay nhiều tùy bạn. Ngọn đèn chỉ sáng đúng mức bạn cần.',
    hints=[('Một gợi ý đầu tiên', 'Một gợi ý nhẹ về ý tưởng cần tìm.'), ('Nhìn kỹ hơn', 'Chỉ ra quân cờ hoặc ô cờ quan trọng.'), ('Chính nước đi', 'Cho bạn thấy nước đi hay nhất để hiểu vì sao nó hiệu quả.')],
    t_eyebrow='Luyện tập', t_h='Từng bước nhỏ, mỗi ngày',
    t_cards=[('Bài học ngắn', 'Bài học tương tác ngắn, vài phút là xong, kèm gợi ý đèn ba mức mỗi khi bạn bí.'),
             ('Câu đố đúng trình độ', 'Chiến thuật, các thế chiếu hết, khai cuộc và tàn cuộc, chọn theo cách bạn chơi.'),
             ('Thử thách hằng ngày và hơn thế', 'Thử thách mỗi ngày, Đường mòn bất tận và giải đấu hằng tuần giữ cho việc luyện tập luôn mới.'),
             ('Xưởng sửa lỗi', 'Ôn lại nước sai biến chính lỗi của bạn thành bài luyện, để mỗi lần trượt chân đều dạy được điều gì đó.')],
    r_eyebrow='Đối thủ', r_h='Những đối thủ biết viết thư',
    r_p='Năm tính cách AI, mỗi người một phong cách, gửi cho bạn thư thách đấu mỗi ngày. Thua một ván, nó có thể quay lại thành trận phục thù.',
    rivals=[('kai', 'Kai'), ('luna', 'Luna'), ('milo', 'Milo'), ('nova', 'Nova'), ('orion', 'Orion')],
    c_eyebrow='Huấn luyện viên', c_h='Huấn luyện viên ngay trên thiết bị, luôn ở bên bạn',
    c_p='Hỏi huấn luyện viên khi đang chơi, nhận gợi ý và xem lại mọi ván sau đó. Sau ván, hãy Hỏi Cư dân để trò chuyện ngắn về lỗi sai, nước đi hay nhất hoặc nên thử gì tiếp theo.',
    c_note='Mọi lời giải thích được tạo ngay trên thiết bị của bạn, dùng Apple Intelligence khi có và dùng mẫu có sẵn nếu không. Việc đánh giá thế cờ luôn do công cụ cờ đảm nhiệm.',
    p_eyebrow='Riêng tư từ thiết kế', p_h='Mọi thứ ở lại trên thiết bị của bạn',
    p_p='Công cụ cờ, huấn luyện viên, ván đấu và thống kê đều chạy trên thiết bị. Ván cờ, ảnh và cuộc trò chuyện với huấn luyện viên không bao giờ rời khỏi đó.',
    p_list=[('Không tài khoản', 'Mở ứng dụng là chơi được ngay.'), ('Không quảng cáo', 'Không bao giờ, ở bất cứ đâu trong ứng dụng.'), ('Không theo dõi', 'Không thu thập dữ liệu dưới bất kỳ hình thức nào.'), ('Chơi được khi offline', 'Trên máy bay hay nơi không có sóng.')],
    fam_eyebrow='Cho cả gia đình', fam_h='Vui tươi cho bé, điềm tĩnh cho người lớn',
    kid_h='Chế độ trẻ em', kid_p='Firefly cổ vũ từng nước đi hay và các quân cờ phản ứng tinh tế trên bàn cờ. Ấm áp, vui tươi và khích lệ.',
    adult_h='Chế độ người lớn', adult_p='Trải nghiệm điềm tĩnh hơn, ưu tiên thống kê, vẫn là huấn luyện viên và những bài học ấy.',
    fam_list=[('Mỗi người một hồ sơ', 'Mỗi người chơi có hồ sơ riêng trên cùng thiết bị, với tiến trình, huy hiệu và nhật ký riêng. Thêm, đổi tên hoặc xóa hồ sơ nằm sau cổng phụ huynh.'),
              ('Góc phụ huynh', 'Báo cáo thời gian chơi dành cho phụ huynh.'),
              ('Dễ tiếp cận', 'Hỗ trợ VoiceOver, Dynamic Type và Giảm chuyển động.'),
              ('Giao diện sáu ngôn ngữ', 'Tiếng Việt, Anh, Tây Ban Nha, Bồ Đào Nha (Brazil), Đức và Pháp. Bài học có tiếng Việt và tiếng Anh.')],
    g_eyebrow='Trong ứng dụng', g_h='Dạo quanh vương quốc', g_prev='Ảnh chụp trước', g_next='Ảnh chụp tiếp theo',
    cap=dict(home='Trang chủ', learn='Bản đồ vương quốc', coach='Huấn luyện viên', review='Xem lại ván', scan='Quét bàn cờ thật', family='Gia đình', festival='Lễ hội', resident='Hỏi Cư dân', training='Luyện tập', game='Chơi cờ'),
    plus_eyebrow='Chess Coach Plus', plus_h='Miễn phí để bắt đầu, Plus khi bạn muốn nhiều hơn',
    plus_free_h='Miễn phí', plus_free=['Chơi cờ', 'Các bài học cơ bản', 'Luyện tập hằng ngày'],
    plus_h2='Plus', plus_list=['Câu đố và luyện lỗi sai không giới hạn', 'Phân tích toàn bộ ván cờ', 'Gợi ý từ huấn luyện viên không giới hạn', 'Mọi bài học: Khai cuộc, Chiến thuật, Tàn cuộc', 'Bộ khai cuộc cho quân Đen', 'Mọi mẫu trong Sân Tàn cuộc', 'Thử thách theo bậc của cư dân', 'Giao diện bàn cờ và bộ quân cao cấp'],
    plus_p='Chọn gói tháng, gói năm (có dùng thử miễn phí) hoặc mua một lần trọn đời. Cả ba đều hỗ trợ Chia sẻ trong gia đình. Giá hiển thị trong ứng dụng theo tiền tệ của bạn.',
    plus_legal='Gói đăng ký tự động gia hạn cho đến khi bạn hủy trong cài đặt Tài khoản Apple; khoản thanh toán được tính vào Tài khoản Apple của bạn.',
    cta_h='Vương quốc đang đợi bạn', cta_p='Nhớ mang theo một chiếc đèn.',
    foot_tag='Học cờ vua như một cuộc phiêu lưu',
)

SHOT_ORDER = ['learn', 'home', 'coach', 'review', 'training', 'resident', 'scan', 'family', 'festival', 'game']
RESIDENTS = ['village-postie', 'cave-minor', 'city-king', 'city-knight', 'city-queen', 'sea-captain', 'temple-theory', 'pass-general', 'port-frenchie', 'sea-lighthouse']
RES_ALT = {'village-postie': 'The village postie', 'cave-minor': 'The miner', 'city-king': 'The king', 'city-knight': 'The knight', 'city-queen': 'The queen', 'sea-captain': 'The sea captain', 'temple-theory': 'The temple scholar', 'pass-general': 'The general', 'port-frenchie': 'A port resident', 'sea-lighthouse': 'The lighthouse keeper'}
RES_ALT_VI = {'village-postie': 'Bác đưa thư làng', 'cave-minor': 'Bác thợ mỏ', 'city-king': 'Nhà vua', 'city-knight': 'Hiệp sĩ mã', 'city-queen': 'Nữ hoàng', 'sea-captain': 'Thuyền trưởng', 'temple-theory': 'Học giả đền thờ', 'pass-general': 'Vị tướng', 'port-frenchie': 'Cư dân hải cảng', 'sea-lighthouse': 'Người gác hải đăng'}


def header(c, page='home'):
    L = c['lang']
    nav = ''.join(f'<a href="{c["home"]}{h}">{t}</a>' for h, t in c['nav']) if page == 'home' else ''
    alt = c['alt_lang']
    return (f'<header class="top"><div class="wrap bar"><a class="brand" href="{c["home"]}"><img src="/assets/icon-128.webp" width="36" height="36" alt="" decoding="async"><span>Chess Coach Kingdom</span></a>'
            f'<nav class="links" aria-label="Main">{nav}<a href="{c["support"]}">{c["support_l"]}</a></nav>'
            f'<a class="langsw" href="{alt[1]}" hreflang="{alt[0]}" lang="{alt[0]}">{alt[2]}</a></div></header>')


def footer(c):
    return (f'<footer class="foot"><div class="wrap foot-in"><div class="foot-brand"><img src="/assets/icon-128.webp" width="44" height="44" alt="" loading="lazy"><div><strong>Chess Coach Kingdom</strong><span>{c["foot_tag"]}</span></div></div>'
            f'<nav class="foot-links" aria-label="Footer"><a href="{c["support"]}">{c["support_l"]}</a><a href="{c["privacy"]}">{c["privacy_l"]}</a><a href="mailto:{EMAIL}">{EMAIL}</a></nav>'
            f'<p class="copy">&copy; 2026 Chess Coach Kingdom</p></div></footer>')


def head(lang, title, desc, path, og=True, extra='', alt=None):
    itunes = (f'<meta name="apple-itunes-app" content="app-id={APP_ID}">' if APP_ID else '<!-- TODO: <meta name="apple-itunes-app" content="app-id=XXXXXXXXX"> once the App Store id is known -->')
    tags = ''
    if alt:
        for hl, hp in alt:
            tags += f'<link rel="alternate" hreflang="{hl}" href="{ORIGIN}{hp}">'
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><meta name="color-scheme" content="dark"><meta name="theme-color" content="#16101c">'
            f'<link rel="canonical" href="{ORIGIN}{path}">{tags}'
            f'<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">{itunes}'
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="Chess Coach Kingdom"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">'
            f'<meta property="og:url" content="{ORIGIN}{path}"><meta property="og:image" content="{ORIGIN}/assets/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(title)}"><meta name="twitter:description" content="{html.escape(desc)}"><meta name="twitter:image" content="{ORIGIN}/assets/og.jpg">'
            f'{FONTS}<link rel="stylesheet" href="/assets/site.css">{extra}</head>')


JS = ('<script>document.documentElement.classList.add("js");(function(){var r=matchMedia("(prefers-reduced-motion: reduce)").matches;'
      'var els=document.querySelectorAll(".rv");if(!("IntersectionObserver" in window)||r){els.forEach(function(e){e.classList.add("in")});}else{'
      'var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target)}})},{threshold:.12});els.forEach(function(e){io.observe(e)});}'
      'var bg=document.querySelector("[data-par]");if(bg&&!r){var t=0;addEventListener("scroll",function(){if(t)return;t=requestAnimationFrame(function(){t=0;var y=Math.min(scrollY,900);bg.style.transform="translate3d(0,"+(y*.18)+"px,0)"})},{passive:true})}'
      'var g=document.querySelector(".gallery");if(g){var pv=document.querySelector(".gal-btn.prev"),nx=document.querySelector(".gal-btn.next");'
      'var up=function(){pv.hidden=g.scrollLeft<8;nx.hidden=g.scrollLeft>g.scrollWidth-g.clientWidth-8};'
      'var go=function(d){g.scrollBy({left:d*g.clientWidth*.7,behavior:r?"auto":"smooth"})};'
      'pv.onclick=function(){go(-1)};nx.onclick=function(){go(1)};g.addEventListener("scroll",up,{passive:true});addEventListener("resize",up);up()}'
      '})();</script>')


def landing(c):
    L = c['lang']
    ra = RES_ALT_VI if L == 'vi' else RES_ALT
    alt = [('en', '/'), ('vi', '/vi/'), ('x-default', '/')]
    cta = (f'<a class="btn gold" href="{APP_STORE_URL}">{c["badge_get"]}</a>' if APP_STORE_URL
           else f'<span class="avail"><span class="dot"></span>{c["avail"]}</span>')
    pills = ''.join(f'<li>{p}</li>' for p in c['pills'])
    shot_dir = c['shot']
    hero_shot = pic(f'shots/{shot_dir}-learn', 'The kingdom map in Chess Coach Kingdom on iPhone', 420, 757, 'phone', lazy=False, fetch=True)
    sparks = ''.join(f'<i style="--x:{x}%;--y:{y}%;--d:{d}s;--s:{s}px"></i>' for x, y, d, s in
                     [(8, 30, 7, 5), (22, 70, 9, 4), (38, 18, 8, 6), (55, 60, 10, 4), (70, 25, 7.5, 5), (84, 55, 9.5, 6), (92, 15, 8.5, 4), (47, 85, 11, 5)])
    out = [head(L, c['title'], c['desc'], c['home'], alt=alt), '<body class="home">', header(c)]
    # ---- hero
    out.append(f'''<main id="top"><section class="hero"><div class="hero-bg" data-par aria-hidden="true">{pic('art/panorama', '', 2400, 432, lazy=False, fetch=True)}</div><div class="hero-fade" aria-hidden="true"></div><div class="sparks" aria-hidden="true">{sparks}</div>
<div class="wrap hero-grid"><div class="hero-copy"><p class="eyebrow">{c['eyebrow']}</p><h1>{c['h1']}</h1><p class="lead">{c['lead']}</p><div class="cta">{cta}</div><ul class="pills">{pills}</ul></div>
<div class="hero-art"><div class="halo" aria-hidden="true"></div>{hero_shot}<img class="ff-hero" src="/assets/firefly/happy.png" alt="Firefly, the lantern-carrying knight" width="320" height="420" decoding="async"></div></div></section>''')
    # ---- kingdom
    reg = ''.join(f'<article class="region rv"><div class="region-img">{pic("art/" + k, "", 640, 1147)}</div><div class="region-txt"><h3>{n}</h3><p>{d}</p></div></article>' for k, n, d in c['regions'])
    res = ''.join(f'<li><img src="/assets/residents/{r}.png" alt="{ra[r]}" width="132" height="190" loading="lazy" decoding="async"></li>' for r in RESIDENTS)
    out.append(f'''<section id="kingdom" class="sec"><div class="wrap"><header class="sec-head rv"><p class="eyebrow">{c['k_eyebrow']}</p><h2>{c['k_h']}</h2><p>{c['k_p']}</p></header>
<div class="regions">{reg}</div>
<div class="residents rv"><div class="residents-txt"><h3>{c['res_h']}</h3><p>{c['res_p']}</p></div><ul class="res-row">{res}</ul></div></div></section>''')
    # ---- firefly
    hints = ''.join(f'<li style="--n:{i + 1}"><span class="lamp" aria-hidden="true"></span><span><b>{i + 1}</b> {t}<small>{d}</small></span></li>' for i, (t, d) in enumerate(c['hints']))
    out.append(f'''<section id="firefly" class="sec night"><div class="wrap split"><div class="ff-stage rv"><div class="halo big" aria-hidden="true"></div><img class="ff-big" src="/assets/firefly/proud.png" alt="Firefly lifting its lantern" width="420" height="560" loading="lazy" decoding="async"><img class="ff-small s1" src="/assets/firefly/giggle.png" alt="" width="150" height="200" loading="lazy" decoding="async"></div>
<div class="split-txt rv"><p class="eyebrow">{c['f_eyebrow']}</p><h2>{c['f_h']}</h2><p>{c['f_p']}</p><h3>{c['hint_h']}</h3><p class="muted">{c['hint_p']}</p><ol class="hints">{hints}</ol></div></div></section>''')
    # ---- train
    cards = ''.join(f'<li class="rv"><h3>{t}</h3><p>{d}</p></li>' for t, d in c['t_cards'])
    out.append(f'''<section id="train" class="sec"><div class="wrap"><header class="sec-head rv"><p class="eyebrow">{c['t_eyebrow']}</p><h2>{c['t_h']}</h2></header><ul class="train-grid">{cards}</ul>
<div class="shotpair rv">{pic(f"shots/{shot_dir}-training", "Training tab", 420, 757, "phone")}{pic(f"shots/{shot_dir}-review", "Game review", 420, 757, "phone")}</div></div></section>''')
    # ---- rivals
    rv = ''.join(f'<li><img src="/assets/rivals/{k}.jpg" alt="{n}" width="180" height="180" loading="lazy" decoding="async"><span>{n}</span></li>' for k, n in c['rivals'])
    out.append(f'''<section id="rivals" class="sec night"><div class="wrap"><header class="sec-head rv"><p class="eyebrow">{c['r_eyebrow']}</p><h2>{c['r_h']}</h2><p>{c['r_p']}</p></header><ul class="rivals rv">{rv}</ul></div></section>''')
    # ---- coach + private
    pl = ''.join(f'<li><b>{t}</b><span>{d}</span></li>' for t, d in c['p_list'])
    out.append(f'''<section id="coach" class="sec"><div class="wrap split rev"><div class="split-txt rv"><p class="eyebrow">{c['c_eyebrow']}</p><h2>{c['c_h']}</h2><p>{c['c_p']}</p><p class="muted">{c['c_note']}</p></div>
<div class="shotpair single rv">{pic(f"shots/{shot_dir}-coach", "The coach in Chess Coach Kingdom", 420, 757, "phone")}</div></div></section>
<section id="private" class="sec band"><div class="wrap"><header class="sec-head rv"><p class="eyebrow">{c['p_eyebrow']}</p><h2>{c['p_h']}</h2><p>{c['p_p']}</p></header><ul class="facts rv">{pl}</ul></div></section>''')
    # ---- family
    fl = ''.join(f'<li><h3>{t}</h3><p>{d}</p></li>' for t, d in c['fam_list'])
    out.append(f'''<section id="family" class="sec"><div class="wrap"><header class="sec-head rv"><p class="eyebrow">{c['fam_eyebrow']}</p><h2>{c['fam_h']}</h2></header>
<div class="modes"><article class="mode kid rv"><h3>{c['kid_h']}</h3><p>{c['kid_p']}</p><img src="/assets/firefly/giggle.png" alt="" width="190" height="250" loading="lazy" decoding="async"></article>
<article class="mode adult rv"><h3>{c['adult_h']}</h3><p>{c['adult_p']}</p><picture><source type="image/webp" srcset="/assets/rivals/orion-lg.webp"><img src="/assets/rivals/orion-lg.jpg" alt="" width="360" height="360" loading="lazy" decoding="async"></picture></article></div>
<ul class="fam-list rv">{fl}</ul></div></section>''')
    # ---- gallery
    items = ''.join(f'<li><figure>{pic(f"shots/{shot_dir}-{k}", c["cap"][k] + " screen", 420, 757, "phone")}<figcaption>{c["cap"][k]}</figcaption></figure></li>' for k in SHOT_ORDER)
    ipd = 'ipad-vi' if L == 'vi' else 'ipad'
    out.append(f'''<section id="gallery" class="sec night"><div class="wrap"><header class="sec-head rv"><p class="eyebrow">{c['g_eyebrow']}</p><h2>{c['g_h']}</h2></header></div><div class="gal"><ul class="gallery" tabindex="0" aria-label="{c['g_h']}">{items}</ul><button class="gal-btn prev" type="button" aria-label="{c['g_prev']}" hidden></button><button class="gal-btn next" type="button" aria-label="{c['g_next']}"></button></div>
<div class="wrap"><div class="ipad rv">{pic(f"shots/{ipd}-home", "Chess Coach Kingdom on iPad", 1000, 1333, "tablet")}{pic(f"shots/{ipd}-learn", "The kingdom map on iPad", 1000, 1333, "tablet")}</div></div></section>''')
    # ---- plus
    free = ''.join(f'<li>{x}</li>' for x in c['plus_free'])
    pls = ''.join(f'<li>{x}</li>' for x in c['plus_list'])
    out.append(f'''<section id="plus" class="sec"><div class="wrap"><header class="sec-head rv"><p class="eyebrow">{c['plus_eyebrow']}</p><h2>{c['plus_h']}</h2></header>
<div class="plans"><div class="plan rv"><h3>{c['plus_free_h']}</h3><ul class="ticks">{free}</ul></div><div class="plan plus rv"><h3>{c['plus_h2']}</h3><ul class="ticks">{pls}</ul></div></div>
<p class="plus-note rv">{c['plus_p']}</p><p class="legal">{c['plus_legal']} <a href="{EULA}" rel="noopener">{c['terms_l']}</a></p></div></section>''')
    # ---- final cta
    out.append(f'''<section class="final"><div class="final-bg" aria-hidden="true">{pic('art/hero', '', 1083, 1125)}</div><div class="wrap final-in rv"><img src="/assets/icon-512.webp" width="96" height="96" alt="" loading="lazy"><h2>{c['cta_h']}</h2><p>{c['cta_p']}</p><div class="cta">{cta}</div></div></section></main>''')
    out.append(footer(c)); out.append(JS); out.append('</body></html>')
    page = ''.join(out)
    return re.sub(r'<img ([^>]*?)src="(/assets/(?:firefly|residents)/[^"]+)\.png"([^>]*)>',
                  r'<picture><source type="image/webp" srcset="\2.webp"><img \1src="\2.png"\3></picture>', page)


# ----------------------------------------------------------------------------------------------- support
SUP = {
    '': dict(lang='en', label='English', title='Support — Chess Coach Kingdom', d='Help with Chess Coach Kingdom: restoring purchases, managing Plus, kids and adult mode, offline play and contact.', h1='Support', lead='Answers to the questions we hear most. Still stuck? Write to us.', mail='Email', home='/', pr='/privacy/en/', prl='Privacy Policy', c='Contact us', faq='Frequently asked questions',
             extra=[('What is the difference between kids mode and adult mode?', 'Kids mode is warm and playful: Firefly cheers your moves and pieces react subtly on the board. Adult mode is calmer and puts your stats first. The coach and lessons are the same in both.'),
                    ('Does it work offline?', 'Yes. The engine, the coach, your games and your stats all run on your device, so you can play and learn without a connection.'),
                    ('How do I turn the voice on or off?', 'The voice commentator is optional. Open Settings in the app to switch it on or off, and use your device volume or silent switch as usual.')]),
    'vi': dict(lang='vi', label='Tiếng Việt', title='Hỗ trợ — Chess Coach Kingdom', d='Hỗ trợ Chess Coach Kingdom: khôi phục giao dịch, quản lý Plus, chế độ trẻ em và người lớn, chơi offline và liên hệ.', h1='Hỗ trợ', lead='Câu trả lời cho những câu hỏi thường gặp nhất. Vẫn chưa ổn? Hãy viết cho chúng tôi.', mail='Email', home='/vi/', pr='/privacy/vi/', prl='Chính sách quyền riêng tư', c='Liên hệ', faq='Câu hỏi thường gặp',
               extra=[('Chế độ trẻ em và chế độ người lớn khác nhau thế nào?', 'Chế độ trẻ em ấm áp và vui tươi: Firefly cổ vũ từng nước đi và các quân cờ phản ứng tinh tế trên bàn. Chế độ người lớn điềm tĩnh hơn, ưu tiên thống kê. Huấn luyện viên và bài học giống nhau ở cả hai.'),
                      ('Ứng dụng có chạy offline không?', 'Có. Công cụ cờ, huấn luyện viên, ván đấu và thống kê đều chạy trên thiết bị, nên bạn có thể chơi và học khi không có kết nối.'),
                      ('Làm sao bật hoặc tắt giọng nói?', 'Giọng bình luận là tùy chọn. Mở Cài đặt trong ứng dụng để bật hoặc tắt, và dùng âm lượng hoặc công tắc im lặng của thiết bị như bình thường.')]),
    'es': dict(lang='es', label='Español', title='Soporte — Chess Coach Kingdom', d='Ayuda con Chess Coach Kingdom: restaurar compras, gestionar Plus, modo infantil y adulto, juego sin conexión y contacto.', h1='Soporte', lead='Respuestas a las preguntas más frecuentes. ¿Sigues atascado? Escríbenos.', mail='Correo', home='/', pr='/privacy/es/', prl='Política de privacidad', c='Contacto', faq='Preguntas frecuentes',
               extra=[('¿Qué diferencia hay entre el modo infantil y el modo adulto?', 'El modo infantil es cálido y divertido: Firefly celebra tus jugadas y las piezas reaccionan con sutileza en el tablero. El modo adulto es más tranquilo y prioriza tus estadísticas. El entrenador y las lecciones son los mismos en ambos.'),
                      ('¿Funciona sin conexión?', 'Sí. El motor, el entrenador, tus partidas y tus estadísticas funcionan en tu dispositivo, así que puedes jugar y aprender sin conexión.'),
                      ('¿Cómo activo o desactivo la voz?', 'La voz del comentarista es opcional. Abre Ajustes en la app para activarla o desactivarla, y usa el volumen o el interruptor de silencio del dispositivo como siempre.')]),
    'fr': dict(lang='fr', label='Français', title='Assistance — Chess Coach Kingdom', d='Aide pour Chess Coach Kingdom : restaurer les achats, gérer Plus, mode enfant et adulte, jeu hors ligne et contact.', h1='Assistance', lead='Les réponses aux questions les plus fréquentes. Toujours bloqué ? Écrivez-nous.', mail='E-mail', home='/', pr='/privacy/fr/', prl='Politique de confidentialité', c='Nous contacter', faq='Questions fréquentes',
               extra=[('Quelle différence entre le mode enfant et le mode adulte ?', 'Le mode enfant est chaleureux et ludique : Firefly encourage vos coups et les pièces réagissent subtilement sur l’échiquier. Le mode adulte est plus calme et met vos statistiques en avant. Le coach et les leçons sont les mêmes dans les deux.'),
                      ('Cela fonctionne-t-il hors ligne ?', 'Oui. Le moteur, le coach, vos parties et vos statistiques fonctionnent sur votre appareil : vous pouvez jouer et apprendre sans connexion.'),
                      ('Comment activer ou désactiver la voix ?', 'La voix du commentateur est facultative. Ouvrez Réglages dans l’app pour l’activer ou la désactiver, et utilisez le volume ou le commutateur silencieux de l’appareil comme d’habitude.')]),
    'de': dict(lang='de', label='Deutsch', title='Support — Chess Coach Kingdom', d='Hilfe zu Chess Coach Kingdom: Käufe wiederherstellen, Plus verwalten, Kinder- und Erwachsenenmodus, Offline-Spiel und Kontakt.', h1='Support', lead='Antworten auf die häufigsten Fragen. Noch nicht weitergekommen? Schreib uns.', mail='E-Mail', home='/', pr='/privacy/de/', prl='Datenschutzerklärung', c='Kontakt', faq='Häufige Fragen',
               extra=[('Was ist der Unterschied zwischen Kinder- und Erwachsenenmodus?', 'Der Kindermodus ist warm und verspielt: Firefly feuert deine Züge an und die Figuren reagieren dezent auf dem Brett. Der Erwachsenenmodus ist ruhiger und stellt deine Statistiken in den Vordergrund. Coach und Lektionen sind in beiden gleich.'),
                      ('Funktioniert die App offline?', 'Ja. Engine, Coach, deine Partien und Statistiken laufen auf deinem Gerät, du kannst also ohne Verbindung spielen und lernen.'),
                      ('Wie schalte ich die Stimme ein oder aus?', 'Die Kommentatorstimme ist optional. Öffne die Einstellungen in der App, um sie ein- oder auszuschalten, und nutze wie gewohnt Lautstärke oder Stummschalter des Geräts.')]),
    'pt-BR': dict(lang='pt-BR', label='Português (Brasil)', title='Suporte — Chess Coach Kingdom', d='Ajuda com o Chess Coach Kingdom: restaurar compras, gerenciar o Plus, modo infantil e adulto, jogo offline e contato.', h1='Suporte', lead='Respostas para as perguntas mais comuns. Ainda travado? Fale conosco.', mail='E-mail', home='/', pr='/privacy/pt-BR/', prl='Política de Privacidade', c='Fale conosco', faq='Perguntas frequentes',
                  extra=[('Qual a diferença entre o modo infantil e o modo adulto?', 'O modo infantil é acolhedor e divertido: o Firefly comemora suas jogadas e as peças reagem de leve no tabuleiro. O modo adulto é mais calmo e prioriza suas estatísticas. O treinador e as lições são os mesmos nos dois.'),
                         ('Funciona offline?', 'Sim. O motor, o treinador, suas partidas e suas estatísticas rodam no seu dispositivo, então você pode jogar e aprender sem conexão.'),
                         ('Como ligo ou desligo a voz?', 'A voz do comentarista é opcional. Abra Ajustes no app para ligar ou desligar e use o volume ou o botão de silêncio do aparelho como de costume.')]),
}
SUP_SHELL = {  # localized chrome for support pages
    '': 'Chess Coach Kingdom', }


def old(path):
    return subprocess.run(['git', '-C', SITE, 'show', f'8ddacc0:{path}'], capture_output=True, text=True, check=True).stdout


def support_page(key, s):
    path = f'support/{key}/index.html' if key else 'support/index.html'
    src = old(path)
    sections = re.findall(r'<details>.*?</details>', src, re.S)
    mail = re.search(r'<h2>[^<]*</h2><p>[^<]*<a href="mailto', src)
    items = sections + [f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in s['extra']]
    # order: restore, cancel, family sharing, kids/adult, offline, voice, profiles, data, bug
    order = [0, 1, 2, 6, 7, 8, 3, 4, 5]
    items = [items[i] for i in order]
    items = [i.replace('<details>', '<details class="faq">') for i in items]
    url = f'/support/{key}/' if key else '/support/'
    langs = ''.join(f'<a href="{"/support/" + k + "/" if k else "/support/"}" hreflang="{v["lang"]}" lang="{v["lang"]}"{" aria-current=page" if k == key else ""}>{v["label"]}</a>' for k, v in SUP.items())
    c = {'lang': s['lang'], 'home': s['home'], 'nav': [], 'support': url, 'support_l': s['h1'], 'privacy': s['pr'], 'privacy_l': s['prl'], 'foot_tag': '', 'alt_lang': ('vi', '/vi/', 'Tiếng Việt') if s['home'] == '/' else ('en', '/', 'English')}
    c['foot_tag'] = (VI if s['lang'] == 'vi' else EN)['foot_tag']
    body = (f'<body class="doc">{header(c, "doc")}<main class="wrap doc-main"><div class="doc-hero"><p class="eyebrow">Chess Coach Kingdom</p><h1>{s["h1"]}</h1><p class="lead">{s["lead"]}</p>'
            f'<a class="btn gold" href="mailto:{EMAIL}">{s["mail"]}: {EMAIL}</a></div>'
            f'<nav class="localesw" aria-label="Language">{langs}</nav><h2 class="h2s">{s["faq"]}</h2><div class="faqs">{"".join(items)}</div>'
            f'<p class="more"><a href="{s["pr"]}">{s["prl"]}</a></p></main>{footer(c)}')
    return head(s['lang'], s['title'], s['d'], url) + body + '</body></html>'


# ----------------------------------------------------------------------------------------------- privacy
PRIV = {'vi': ('vi', 'Tiếng Việt'), 'en': ('en', 'English'), 'es': ('es', 'Español'), 'fr': ('fr', 'Français'), 'de': ('de', 'Deutsch'), 'pt-BR': ('pt-BR', 'Português (Brasil)')}


CONTACT = {'en': 'For questions about this policy, email', 'vi': 'Nếu có câu hỏi, hãy gửi email tới', 'es': 'Para preguntas sobre esta política, escribe a',
           'fr': 'Pour toute question, écrivez à', 'de': 'Bei Fragen zu dieser Erklärung schreibe eine E-Mail an', 'pt-BR': 'Para dúvidas sobre esta política, escreva para'}
UPDATED = {'en': '2026-10-10', 'vi': '10-10-2026', 'es': '2026-10-10', 'fr': '10/10/2026', 'de': '10.10.2026', 'pt-BR': '10/10/2026'}


def privacy_page(k):
    src = old(f'privacy/{k}/index.html')
    src = re.sub(r'(<em>[^<:]*:\s*)[^<]*(</em>)', lambda m: m.group(1) + UPDATED[k] + m.group(2), src, count=1)
    src, n = re.subn(r'(<h2>[^<]*</h2>)\s*<p>[^<]*</p>\s*<p><a href="https://github[^<]*</a></p>', lambda m: m.group(1) + f'<p>{CONTACT[k]} <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>', src)
    assert n == 1, k
    title = re.search(r'<title>(.*?)</title>', src).group(1)
    inner = re.search(r'<main>(.*)</main>', src, re.S).group(1)
    inner = re.sub(r'^<nav>.*?</nav>', '', inner, count=1, flags=re.S)  # replaced by the shared locale switcher
    def _tbl(m):
        cells = [x.strip() for x in m.group(1).split('|') if x.strip() and x.strip() != '---']
        rows = [cells[i:i + 2] for i in range(0, len(cells), 2)]
        th = ''.join(f'<th>{x}</th>' for x in rows[0])
        tr = ''.join('<tr>' + ''.join(f'<td>{x}</td>' for x in r) + '</tr>' for r in rows[1:])
        return f'<div class="tbl"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
    inner = re.sub(r'<p>(\|[^<]*\|---\|[^<]*)</p>', _tbl, inner)
    langs = ''.join(f'<a href="/privacy/{kk}/" hreflang="{l}" lang="{l}"{" aria-current=page" if kk == k else ""}>{n}</a>' for kk, (l, n) in PRIV.items())
    ctx = VI if k == 'vi' else EN
    c = {'lang': k, 'home': '/vi/' if k == 'vi' else '/', 'nav': [], 'support': '/support/vi/' if k == 'vi' else f'/support/{k}/' if k in SUP else '/support/',
         'support_l': {'vi': 'Hỗ trợ', 'es': 'Soporte', 'fr': 'Assistance', 'de': 'Support', 'pt-BR': 'Suporte'}.get(k, 'Support'),
         'privacy': f'/privacy/{k}/', 'privacy_l': title.split(' — ')[0], 'foot_tag': ctx['foot_tag'], 'alt_lang': ('vi', '/vi/', 'Tiếng Việt') if k != 'vi' else ('en', '/', 'English')}
    body = f'<body class="doc lp">{header(c, "doc")}<main class="wrap doc-main prose"><nav class="localesw" aria-label="Language">{langs}</nav>{inner}</main>{footer(c)}'
    h = head(k, title, title, f'/privacy/{k}/')
    return h + body + '</body></html>'


def write(path, content):
    p = SITE + path
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(content)


def notfound():
    c = dict(EN, nav=[])
    return (head('en', 'Page not found — Chess Coach Kingdom', 'This page could not be found.', '/404.html').replace('</head>', '<meta name="robots" content="noindex"></head>')
            + f'<body class="doc nf">{header(c, "doc")}<main class="nf-main"><div class="hero-bg" aria-hidden="true">{pic("art/panorama", "", 2400, 432, lazy=False)}</div><div class="hero-fade" aria-hidden="true"></div>'
              '<div class="wrap nf-in"><img class="ff-nf" src="/assets/firefly/worried.png" alt="Firefly looking worried" width="220" height="290"><p class="eyebrow">404</p><h1>This path leads nowhere</h1><p class="lead">Firefly looked everywhere with the lantern, but this page is not in the kingdom.</p>'
              '<a class="btn gold" href="/">Back to the kingdom</a></div></main>' + footer(c) + '</body></html>')


if __name__ == '__main__':
    write('index.html', landing(EN))
    write('vi/index.html', landing(VI))
    for k, s in SUP.items():
        write(f'support/{k}/index.html' if k else 'support/index.html', support_page(k, s))
    for k in PRIV:
        write(f'privacy/{k}/index.html', privacy_page(k))
    write('404.html', notfound())
    write('privacy/index.html', head('en', 'Privacy Policy — Chess Coach Kingdom', 'Chess Coach Kingdom privacy policy.', '/privacy/').replace('</head>', '<script>var l=(navigator.language||"en").toLowerCase(),m={vi:"vi",es:"es",fr:"fr",de:"de",pt:"pt-BR"},k=l.split("-")[0];location.replace("/privacy/"+(m[k]||"en")+"/");</script><meta http-equiv="refresh" content="1;url=/privacy/en/"></head>')
          + '<body class="doc"><main class="wrap doc-main"><h1>Privacy Policy</h1><p class="lead">Redirecting to your language&hellip;</p><nav class="localesw" aria-label="Language">' + ''.join(f'<a href="/privacy/{kk}/" hreflang="{l}" lang="{l}">{n}</a>' for kk, (l, n) in PRIV.items()) + '</nav></main></body></html>')
    print('ok')
