import json
import random
import uuid

def generate_sql():
    quests = [
        # --- CONFIDENCE & SOCIAL COURAGE (Category: confidence) ---
        ("Bắt đầu cuộc trò chuyện", "Start a Conversation", "Làm quen và nói chuyện với một người lạ hoặc đồng nghiệp ít tiếp xúc.", "Introduce yourself and talk to a stranger or a rarely spoken colleague.", "main", "confidence", 30, {"confidence": 4, "social_courage": 6}),
        ("Phát biểu ý kiến", "Voice Your Opinion", "Đưa ra ý kiến hoặc đặt câu hỏi trong một cuộc họp hoặc lớp học.", "Share an opinion or ask a question during a meeting or class.", "main", "confidence", 35, {"confidence": 5, "social_courage": 5}),
        ("Khen ngợi chân thành", "Genuine Compliment", "Đưa ra lời khen ngợi chân thành cho 3 người khác nhau trong hôm nay.", "Give a genuine compliment to 3 different people today.", "side", "confidence", 25, {"social_courage": 4, "mental_resilience": 2}),
        ("Mời đi cà phê", "Coffee Invite", "Mời một người bạn hoặc đồng nghiệp đi uống nước để gắn kết.", "Invite a friend or colleague for a drink to bond.", "main", "confidence", 30, {"social_courage": 5, "consistency": 2}),
        ("Giao tiếp bằng mắt", "Eye Contact Mastery", "Duy trì giao tiếp bằng mắt vững vàng trong tất cả các cuộc trò chuyện hôm nay.", "Maintain steady eye contact in all conversations today.", "habit", "confidence", 25, {"confidence": 6}),
        ("Từ chối khéo léo", "Graceful Refusal", "Nói 'Không' một cách lịch sự với một yêu cầu không hợp lý hoặc làm mất thời gian.", "Politely say 'No' to an unreasonable or time-consuming request.", "main", "confidence", 40, {"confidence": 5, "mental_resilience": 4}),
        ("Gọi điện thay vì nhắn tin", "Call Instead of Text", "Thực hiện một cuộc gọi điện thoại cho việc mà bạn thường chỉ nhắn tin.", "Make a phone call for something you would usually just text.", "side", "confidence", 25, {"social_courage": 4}),
        ("Tham gia sự kiện xã hội", "Attend Social Event", "Tham gia vào một buổi tụ tập, meetup hoặc sự kiện nhỏ để mở rộng mối quan hệ.", "Attend a gathering, meetup, or small event to expand your network.", "challenge", "confidence", 50, {"social_courage": 8, "confidence": 4}),
        ("Chia sẻ câu chuyện", "Share a Story", "Kể lại một trải nghiệm cá nhân của bạn cho một nhóm bạn hoặc trong một buổi nói chuyện.", "Tell a personal experience to a group of friends or in a discussion.", "main", "confidence", 35, {"confidence": 4, "social_courage": 4}),
        ("Bảo vệ quan điểm", "Defend Your View", "Tranh luận một cách xây dựng để bảo vệ quan điểm cá nhân mà không bị kích động.", "Debate constructively to defend your personal view without getting emotional.", "main", "confidence", 45, {"confidence": 5, "mental_resilience": 5}),
        ("Thuyết trình ngắn", "Mini Presentation", "Trình bày về một chủ đề bạn am hiểu cho đồng nghiệp, bạn bè hoặc tự quay video.", "Present a topic you know well to peers, or record a video of yourself.", "challenge", "confidence", 50, {"confidence": 7, "knowledge": 3}),
        ("Xung phong nhận việc", "Volunteer for Task", "Xung phong lãnh đạo hoặc nhận một nhiệm vụ mới trong công việc/học tập.", "Volunteer to lead or take on a new task at work/school.", "main", "confidence", 45, {"confidence": 6, "discipline": 3}),
        ("Mặc trang phục nổi bật", "Bold Outfit", "Mặc một bộ trang phục mà bạn thích nhưng trước đây ngại mặc ra ngoài.", "Wear an outfit you like but were previously too shy to wear outside.", "habit", "confidence", 25, {"confidence": 5}),
        ("Phỏng vấn người lạ", "Stranger Interview", "Hỏi đường hoặc nhờ sự giúp đỡ ngắn từ một người không quen biết.", "Ask for directions or brief help from someone you don't know.", "side", "confidence", 20, {"social_courage": 4}),
        ("Đăng bài tự hào", "Proud Post", "Chia sẻ một thành tựu nhỏ của bạn lên mạng xã hội hoặc nhóm với bạn bè.", "Share a small achievement on social media or with a group of friends.", "side", "confidence", 20, {"confidence": 4}),
        ("Đối mặt với nỗi sợ trần tục", "Face a Mundane Fear", "Làm một việc nhỏ khiến bạn cảm thấy e dè (vd: trả giá, gọi phản ánh dịch vụ).", "Do a small thing that makes you timid (e.g., bargaining, complaining about service).", "main", "confidence", 40, {"confidence": 6, "social_courage": 4}),
        ("Xin feedback", "Ask for Feedback", "Chủ động xin phản hồi về công việc hoặc kỹ năng của bạn từ một người đi trước.", "Proactively ask for feedback on your work or skills from a senior.", "main", "confidence", 35, {"confidence": 4, "wisdom": 4}),
        ("Xưng hô tự tin", "Confident Posture", "Thực hành đi bộ và ngồi với tư thế thẳng lưng, ngực mở rộng trong suốt cả ngày.", "Practice walking and sitting with a straight back and open chest all day.", "habit", "confidence", 25, {"confidence": 5, "consistency": 2}),
        ("Tham gia CLB mới", "Join New Club", "Đăng ký tham gia một câu lạc bộ hoặc nhóm trực tuyến có chung sở thích.", "Sign up for a club or online group sharing your interests.", "challenge", "confidence", 45, {"social_courage": 6, "exploration": 3}),
        ("Dẫn dắt cuộc chơi", "Lead the Game", "Tổ chức một buổi đi chơi, chơi game board hoặc một hoạt động chung.", "Organize an outing, board game session, or group activity.", "main", "confidence", 40, {"social_courage": 5, "confidence": 4}),

        # --- CONSISTENCY & DISCIPLINE (Category: discipline) ---
        ("Chuỗi thói quen", "Habit Chain", "Thực hiện thành công 3 thói quen buổi sáng liên tiếp mà không trì hoãn.", "Successfully execute 3 morning habits in a row without procrastination.", "habit", "discipline", 30, {"consistency": 6, "discipline": 4}),
        ("Bám sát lịch trình", "Stick to Schedule", "Hoàn thành 100% các công việc trong to-do list hôm nay.", "Complete 100% of the tasks on today's to-do list.", "main", "discipline", 45, {"consistency": 7, "discipline": 5}),
        ("Không đường hôm nay", "No Sugar Today", "Tránh hoàn toàn các loại đồ uống và thức ăn chứa nhiều đường trong ngày.", "Completely avoid high-sugar foods and drinks for the day.", "challenge", "discipline", 35, {"consistency": 5, "mental_resilience": 4}),
        ("Đúng giờ tuyệt đối", "Absolute Punctuality", "Đến sớm 5 phút cho mọi cuộc hẹn, lớp học hoặc cuộc họp trong hôm nay.", "Arrive 5 minutes early for all appointments, classes, or meetings today.", "habit", "discipline", 30, {"consistency": 6, "social_courage": 2}),
        ("Gọn gàng trước khi ngủ", "Tidy Before Bed", "Dành 15 phút dọn dẹp bàn làm việc và phòng trí trước khi đi ngủ.", "Spend 15 minutes organizing your desk and room before sleeping.", "habit", "discipline", 25, {"consistency": 4, "discipline": 3}),
        ("Đọc sách liên tục", "Read Consistently", "Đọc sách ít nhất 30 phút vào đúng một khung giờ cố định trong ngày.", "Read for at least 30 minutes at exactly the scheduled time today.", "main", "discipline", 30, {"consistency": 5, "wisdom": 4}),
        ("Không mạng xã hội sáng", "No Morning Social Media", "Không chạm vào mạng xã hội trong 2 giờ đầu tiên sau khi thức dậy.", "Do not touch social media for the first 2 hours after waking up.", "challenge", "discipline", 40, {"consistency": 5, "focus": 5}),
        ("Hoàn thành việc đáng ghét", "Eat the Frog", "Hoàn thành công việc khó khăn và bị trì hoãn lâu nhất ngay trong buổi sáng.", "Complete the hardest and most procrastinated task first thing in the morning.", "main", "discipline", 50, {"discipline": 8, "consistency": 4}),
        ("Lập ngân sách", "Budget Tracking", "Ghi chép và phân tích toàn bộ chi tiêu của ngày hôm nay vào buổi tối.", "Record and analyze all expenses of the day in the evening.", "habit", "discipline", 25, {"consistency": 5, "knowledge": 2}),
        ("Quy tắc 2 phút", "2-Minute Rule", "Thực hiện ngay lập tức bất kỳ công việc nào có thể hoàn thành dưới 2 phút.", "Do immediately any task that can be completed in under 2 minutes.", "habit", "discipline", 25, {"consistency": 4, "discipline": 4}),
        ("Bữa ăn tự nấu", "Home Cooked Meal", "Tự chuẩn bị nấu một bữa ăn lành mạnh thay vì ăn ngoài hoặc order.", "Cook a healthy meal yourself instead of eating out or ordering.", "main", "discipline", 35, {"consistency": 4, "stamina": 3}),
        ("Viết nhật ký kiên định", "Consistent Journaling", "Viết ít nhất 1 trang nhật ký liên tục suy ngẫm về những gì đã học được.", "Write at least 1 page of journal reflecting on what you learned.", "habit", "discipline", 30, {"consistency": 5, "mental_resilience": 3}),
        ("Nói không với YouTube", "YouTube Detox", "Không xem bất kỳ video giải trí nào trên YouTube trong suốt 24 giờ.", "Do not watch any entertainment videos on YouTube for 24 hours.", "challenge", "discipline", 40, {"consistency": 6, "focus": 4}),
        ("Theo dõi lượng nước", "Hydration Tracking", "Uống đủ 2.5 lít nước và theo dõi từng ly.", "Drink 2.5 liters of water and track every glass.", "habit", "discipline", 20, {"consistency": 4, "stamina": 2}),
        ("Không than vãn", "No Complaining", "Trải qua 24 giờ không nói ra hoặc gõ phím bất kỳ lời phàn nàn, than vãn nào.", "Go 24 hours without voicing or typing any complaints.", "challenge", "discipline", 45, {"consistency": 6, "mental_resilience": 6}),
        ("Ngủ đúng giờ", "Curfew Master", "Tắt toàn bộ thiết bị điện tử lúc 10.30PM và lên giường lúc 11PM.", "Turn off all electronics at 10.30 PM and be in bed by 11 PM.", "main", "discipline", 40, {"consistency": 7, "stamina": 3}),
        ("Dậy ngay khi báo thức", "First Alarm Wake", "Thức dậy ngay ở tiếng chuông báo thức đầu tiên, không ấn nút báo lại.", "Wake up at the first alarm ring, no snooze.", "habit", "discipline", 30, {"consistency": 5, "discipline": 5}),
        ("Tối giản hóa", "Declutter", "Xóa bớt 50 tệp tin rác trong máy tính hoặc vứt bỏ 5 món đồ không dùng tới.", "Delete 50 junk files on your PC or throw away 5 unused items.", "side", "discipline", 25, {"consistency": 4, "focus": 2}),
        ("Đánh giá ngày", "Daily Review", "Dành 10 phút trước khi ngủ để đánh giá mức độ kiên định của hôm nay.", "Spend 10 mins before bed reviewing your consistency matrix for today.", "habit", "discipline", 20, {"consistency": 4, "wisdom": 2}),
        ("Chuẩn bị trước", "Prepare Ahead", "Chuẩn bị quần áo và túi xách cho ngày mai từ tối hôm trước.", "Prepare clothes and bag for tomorrow the night before.", "habit", "discipline", 20, {"consistency": 5}),

        # --- FITNESS & STAMINA (Category: fitness) ---
        ("Chạy bộ vượt giới hạn", "Exceed Running Limit", "Chạy hoặc đi bộ nhanh vượt quá kỉ lục khoảng cách gần đây của bạn 10%.", "Run or brisk walk 10% further than your recent distance record.", "challenge", "fitness", 40, {"stamina": 6, "consistency": 3}),
        ("Cardio cường độ cao", "HIIT Cardio", "Tập một bài HIIT Cardio đẫm mồ hôi trong 20 phút.", "Perform a sweat-inducing 20-minute HIIT Cardio workout.", "main", "fitness", 35, {"stamina": 5, "strength": 3}),
        ("Đẩy năng lực cơ thể", "Push-up Mastery", "Hoàn thành 5 hiệp hít đất, mỗi hiệp tập đến mức gần như không thể nâng nữa.", "Complete 5 sets of push-ups, each to near failure.", "main", "fitness", 45, {"strength": 7, "mental_resilience": 3}),
        ("Core Thép", "Steel Core", "Thực hiện chuỗi bài tập bụng (Plank, Crunches, Leg raises) trong 15 phút không nghỉ dài.", "Do an ab workout circuit for 15 minutes without long rests.", "main", "fitness", 30, {"strength": 4, "stamina": 3}),
        ("Leo cầu thang", "Stairway to Health", "Sử dụng cầu thang bộ thay vì thang máy trong mọi tình huống hôm nay.", "Use the stairs instead of the elevator in all situations today.", "habit", "fitness", 25, {"stamina": 5, "consistency": 4}),
        ("Yoga phục hồi", "Recovery Yoga", "Tập 30 phút Hatha Yoga hoặc giãn cơ sâu để phục hồi cơ thể.", "Do 30 mins of Hatha Yoga or deep stretching for recovery.", "side", "fitness", 25, {"stamina": 3, "mental_resilience": 2}),
        ("Gánh đùi sắt đá", "Iron Squats", "Hoàn thành tổng cộng 150 cái squats chia làm nhiều hiệp trong ngày.", "Complete a total of 150 squats divided into multiple sets today.", "challenge", "fitness", 40, {"strength": 6, "stamina": 3}),
        ("Nhảy dây diệt mỡ", "Jump Rope Burn", "Nhảy dây 1000 cái (hoặc 15 phút tập liên tục).", "Do 1000 jump ropes (or jump continuously for 15 minutes).", "main", "fitness", 35, {"stamina": 6, "focus": 2}),
        ("Đi bộ 10k bước", "10k Steps", "Đạt tròn 10,000 bước đi bộ trước 9 giờ tối.", "Hit exactly 10,000 steps before 9 PM.", "habit", "fitness", 30, {"stamina": 4, "consistency": 4}),
        ("Tập lưng xô", "Pull-up / Back Day", "Hoàn thành một buổi tập hít xà hoặc kéo xô tối thiểu 30 phút.", "Complete a pull-up or back workout session for at least 30 mins.", "main", "fitness", 40, {"strength": 6, "consistency": 2}),
        ("Tập sáng sớm", "Morning Workout", "Thức dậy và hoàn thành bài tập thể dục buổi sáng trước khi ăn sáng.", "Wake up and finish a morning workout before breakfast.", "challenge", "fitness", 45, {"stamina": 4, "consistency": 6}),

        # --- WISDOM & KNOWLEDGE (Category: wisdom) ---
        ("Đọc tài liệu chuyên sâu", "Read Deep Article", "Đọc và ghi chú lại một bài báo cáo khoa học hoặc bài viết chuyên môn dài rèn trí tuệ.", "Read and note down insights from a long scientific or professional article.", "main", "wisdom", 35, {"knowledge": 5, "wisdom": 4}),
        ("Học từ vựng mới", "Vocab Builder", "Học sâu 10 từ vựng/thuật ngữ ngoại ngữ mới và đặt câu thực tế với chúng.", "Deeply learn 10 new foreign words/terms and make real sentences.", "habit", "wisdom", 30, {"knowledge": 4, "consistency": 3}),
        ("Học khóa học online", "Online Course Progress", "Hoàn thành 2 bài giảng hoặc 45 phút học trong khóa học Udemy/Coursera đang dang dở.", "Finish 2 lectures or 45 mins of a pending online course.", "main", "wisdom", 40, {"knowledge": 6, "focus": 3}),
        ("Nghe Podcast giáo dục", "Educational Podcast", "Nghe một podcast về lịch sử, khoa học, hoặc phát triển bản thân khi đang đi lại.", "Listen to a history, science, or self-help podcast while commuting.", "side", "wisdom", 25, {"wisdom": 4, "knowledge": 2}),
        ("Ôn lại kiến thức cũ", "Review Old Notes", "Mở lại sổ tay hoặc Notion cũ, ôn lại và tổng hợp một chủ đề bạn từng học.", "Open old notes, review and synthesize a topic you studied before.", "main", "wisdom", 35, {"knowledge": 5, "consistency": 3}),
        ("Tóm tắt sách", "Book Summary", "Viết một tóm tắt dài 300 từ cho chương sách vừa đọc xong.", "Write a 300-word summary for the chapter you just finished reading.", "challenge", "wisdom", 45, {"wisdom": 6, "focus": 4}),
        ("Học một kỹ năng nhỏ", "Micro-learning", "Xem một video hướng dẫn (tutorial) và thực hành ngay một kĩ năng phần mềm nhỏ (VD Excel, Photoshop).", "Watch a tutorial and immediately practice a small software skill.", "main", "wisdom", 30, {"knowledge": 5, "focus": 2}),
        ("Giải đố Logic", "Logic Puzzles", "Hoàn thành 5 bài toán logic, Sudoku mức khó hoặc chơi cờ vua.", "Complete 5 logic puzzles, hard Sudoku or play chess.", "side", "wisdom", 25, {"wisdom": 4, "focus": 3}),
        ("Khám phá triết học", "Philosophy Insight", "Tìm hiểu về một triết lý mới (như Khắc kỷ - Stoicism) và áp dụng vào 1 việc hôm nay.", "Learn about a philosophy (like Stoicism) and apply it to 1 thing today.", "main", "wisdom", 40, {"wisdom": 7, "mental_resilience": 3}),
        ("Viết blog / ghi chép dài", "Write Blog Post", "Viết một bài phân tích dài hoặc note chi tiết về một chủ đề bạn đúc kết được.", "Write a long analysis or detailed note about a topic you concluded.", "challenge", "wisdom", 50, {"wisdom": 6, "knowledge": 6}),

        # --- FOCUS & MENTAL RESILIENCE (Category: focus) ---
        ("Pomodoro siêu tập trung", "Deep Pomodoro", "Hoàn thành 4 chu kỳ Pomodoro (25 phút) liên tục trong yên lặng tuyệt đối.", "Complete 4 Pomodoro cycles (25 mins) continuously in absolute silence.", "main", "focus", 45, {"focus": 8, "discipline": 4}),
        ("Chống lại cám dỗ", "Resist the Urge", "Khi bạn cực kì muốn lướt mạng hoặc ăn vặt, dập tắt ý muốn đó và quay lại làm việc.", "When you crave scrolling or snacking, kill the urge and return to work.", "habit", "focus", 30, {"mental_resilience": 6, "consistency": 3}),
        ("Thiền định sâu", "Deep Meditation", "Ngồi thiền 20 phút không phản ứng với bất kỳ tiếng ồn hay suy nghĩ nào ngắt ngang.", "Sit in meditation for 20 mins, reacting to no distracting sounds or thoughts.", "main", "focus", 35, {"focus": 6, "mental_resilience": 5}),
        ("Làm việc với nhạc sóng não", "Binaural Focus", "Sử dụng nhạc sóng não (Binaural beats, không lời) để duy trì sự tập trung suốt 1 giờ.", "Use binaural beats to maintain focus for 1 full hour.", "side", "focus", 25, {"focus": 5}),
        ("Thiết lập ranh giới", "Set Boundaries", "Đóng toàn bộ tab không liên quan và để điện thoại xa khỏi tầm với trong 2 tiếng.", "Close all irrelevant tabs and put your phone out of reach for 2 hours.", "main", "focus", 40, {"focus": 7, "consistency": 4}),
        ("Phân tích lỗi sai", "Mistake Evaluation", "Chấp nhận một lỗi sai nhỏ hôm nay, không tự trách mà ghi chú cách giải quyết hợp lý.", "Accept a small mistake today, don't blame yourself, but note a solution.", "habit", "focus", 25, {"mental_resilience": 5, "wisdom": 3}),
        ("Tắm nước lạnh", "Cold Shower", "Tắm nước bằng nhiệt độ lạnh nhất có thể trong 3 phút để rèn luyện tinh thần sắt đá.", "Take a shower at the coldest temp for 3 minutes to forge mental toughness.", "challenge", "focus", 45, {"mental_resilience": 8, "confidence": 3}),
        ("Hô hấp hộp", "Box Breathing", "Khi căng thẳng hoặc trước khi làm việc khó, thực hiện kĩ thuật thở Box Breathing 5 lần.", "When stressed or before tough tasks, do Box Breathing 5 times.", "habit", "focus", 20, {"mental_resilience": 4, "focus": 3}),
        ("Giải nén não bộ", "Brain Dump", "Viết mọi suy nghĩ lộn xộn trong đầu ra giấy trong 10 phút, không cần cấu trúc.", "Write all messy thoughts out on paper for 10 mins, no structure needed.", "side", "focus", 20, {"focus": 4, "mental_resilience": 2}),
        ("Thử thách sự nhàm chán", "Boredom Challenge", "Ngồi yên không làm gì, không dùng điện thoại, không nhạc trong 15 phút.", "Sit completely doing nothing, no phone, no music for 15 mins.", "challenge", "focus", 35, {"mental_resilience": 6, "focus": 5}),

        # --- EXPLORATION & NEW EXPERIENCES (Category: exploration) ---
        ("Tìm đường mới", "New Route", "Đi đến một địa điểm quen thuộc bằng một tuyến đường hoàn toàn mới để kích thích não bộ.", "Go to a familiar place using a completely new route to stimulate the brain.", "side", "exploration", 20, {"knowledge": 3, "exploration": 5}),
        ("Thử đồ ăn lạ", "Try Foreign Cuisine", "Nếm thử một món ăn hoặc đồ uống mà bạn chưa bao giờ thử trước đây.", "Taste a food or drink you have never tried before.", "side", "exploration", 20, {"social_courage": 2, "exploration": 5}),
        ("Đọc một chủ đề ngẫu nhiên", "Random Topic Read", "Click vào tùy chọn 'Bài viết ngẫu nhiên' trên Wikipedia và đọc hết bài đó.", "Click 'Random article' on Wikipedia and read it completely.", "habit", "exploration", 25, {"knowledge": 4, "wisdom": 2}),
        ("Xem phim tài liệu độc lạ", "Unique Documentary", "Xem một tập phim tài liệu về một nền văn hóa hoặc sinh vật mà bạn không biết tới.", "Watch a documentary about a culture or creature you know nothing about.", "main", "exploration", 30, {"knowledge": 5, "focus": 2}),
        ("Thăm một địa điểm văn hóa", "Visit Cultural Spot", "Ghé thăm bảo tàng, phòng tranh, hoặc triển lãm nghệ thuật trong khu vực.", "Visit a local museum, art gallery, or exhibition.", "challenge", "exploration", 45, {"knowledge": 4, "social_courage": 3}),
        ("Nghe nhạc ngôn ngữ khác", "Foreign Music", "Nghe thử một playlist nhạc xu hướng của một quốc gia hoàn toàn xa lạ (vd: Pháp, Arab, Ấn Độ).", "Listen to a trending playlist of a foreign country (e.g., France, Arab, India).", "side", "exploration", 20, {"exploration": 4, "knowledge": 2}),
        ("Kết bạn với ChatGPT", "AI Exploration", "Yêu cầu AI hướng dẫn tóm tắt một khái niệm khoa học cực khó (như Vật lý lượng tử) theo kiểu cho con nít.", "Ask AI to explain a hard science concept like quantum physics like you're 5.", "side", "exploration", 20, {"knowledge": 5, "wisdom": 3}),
        ("Phát hiện 3 điều lạ", "Spot 3 Anomalies", "Quan sát xung quanh trên đường đi và tìm ra 3 chi tiết thú vị mà bạn chưa từng để ý.", "Observe your commute and spot 3 interesting details you never noticed.", "habit", "exploration", 20, {"focus": 3, "exploration": 4}),
        ("Xem kĩ năng sống sót", "Survival Skill Video", "Tìm hiểu một kĩ năng sinh tồn khẩn cấp trên Youtube (tạo lửa, sơ cứu tai nạn).", "Learn an emergency survival skill on Youtube (making fire, first aid).", "main", "exploration", 35, {"knowledge": 5, "mental_resilience": 3}),
        ("Giao tiếp bằng ngôn ngữ khác", "Foreign Interaction", "Sử dụng một vài câu bằng ngoại ngữ mới học để chào hỏi nhân viên quán nước hoặc người quen.", "Use a few phrases of a new language to greet a barista or acquaintance.", "challenge", "exploration", 40, {"social_courage": 6, "knowledge": 4}),
        
        # Thêm các nhiệm vụ hỗ trợ Tự tin và Kiên định để đủ ~100
        ("Thiết lập mục tiêu nhỏ", "Small Goal Setting", "Viết ra 3 mục tiêu siêu nhỏ dễ đạt được hôm nay và hoàn thành chúng trước buổi trưa.", "Write down 3 tiny achievable goals today and finish them before noon.", "habit", "confidence", 25, {"consistency": 4, "confidence": 3}),
        ("Giữ vững lập trường", "Hold Your Ground", "Bảo vệ quyết định của mình khi có người cố gắng làm bạn lung lay trong vấn đề nhỏ.", "Defend your decision when someone tries to sway you on a small issue.", "main", "confidence", 35, {"confidence": 5, "consistency": 4}),
        ("Sửa tư thế ngay lập tức", "Instant Posture Fix", "Mỗi khi nhận ra mình đang khom lưng, lập tức ngồi thẳng và giữ yên trong 5 phút.", "Whenever you catch yourself slouching, immediately sit straight for 5 mins.", "habit", "discipline", 25, {"consistency": 4, "confidence": 3}),
        ("Học cách mỉm cười", "Smile Practice", "Mỉm cười thân thiện với 3 người không quen biết khi đi trên đường hoặc hành lang.", "Smile amicably at 3 strangers while walking on the street or hallway.", "side", "confidence", 25, {"social_courage": 5, "confidence": 3}),
        ("Chỉn chu ngoại hình", "Appearance Polish", "Dành thêm 5 phút buổi sáng để chăm chút kĩ hơn cho tóc tai, quần áo trước khi ra khỏi nhà.", "Spend 5 extra mins in the morning grooming hair and clothes before leaving.", "habit", "confidence", 20, {"consistency": 3, "confidence": 4}),
        ("Bắt đầu dự án bị bỏ dở", "Resume Abandoned Project", "Mở lại một công việc nghệ thuật/kĩ thuật đã bỏ dở và tập trung làm 30 phút.", "Reopen an abandoned art/tech project and focus on it for 30 minutes.", "main", "discipline", 45, {"consistency": 6, "mental_resilience": 4}),
        ("Xây dựng lại chuỗi kỷ lục", "Rebuild the Streak", "Hoàn thành 3 Daily Quest ngay cả khi hôm qua bạn bị mất chuỗi.", "Complete 3 Daily Quests even if you broke your streak yesterday.", "challenge", "discipline", 50, {"consistency": 8, "mental_resilience": 5}),
        ("Thuyết phục thành công", "Successful Persuasion", "Thuyết phục bạn bè hoặc gia đình làm theo 1 ý kiến tích cực của bạn (đi dạo, ăn uống healthy).", "Convince friends or family to follow a positive idea (walking, eating healthy).", "main", "confidence", 40, {"social_courage": 5, "confidence": 4}),
        ("Nói trước gương", "Mirror Speech", "Tập nói rõ ràng, dõng dạc trước gương 5 phút về những gì mình tự hào nhất.", "Practice speaking clearly and loudly in the mirror for 5 mins about what you're proud of.", "habit", "confidence", 30, {"confidence": 6, "mental_resilience": 3}),
        ("Bỏ qua lỗi lầm nhỏ", "Ignore Petty Mistakes", "Không chỉ trích hoặc cáu gắt khi người khác mắc lỗi nhỏ xoàng xĩnh 3 lần trong ngày.", "Do not criticize or get annoyed when others make 3 petty mistakes today.", "habit", "discipline", 30, {"consistency": 4, "social_courage": 3})
    ]

    # Generate SQL file
    sql_lines = []
    sql_lines.append("-- === UPDATE GAME DATA: 70+ NEW QUESTS WITH 1.5x STAT REWARDS ===")
    sql_lines.append("-- Focus on Confidence, Social Courage, and Consistency")
    sql_lines.append("BEGIN;")
    
    for vi, en, d_vi, d_en, qt, cat, exp, stats_dict in quests:
        stat_json = json.dumps(stats_dict)
        # Using gen_random_uuid() to automatically generate an ID in PostgreSQL
        sql_lines.append(f"""INSERT INTO quests (id, title_vi, title_en, description_vi, description_en, quest_type, category, difficulty_min_level, difficulty_max_level, exp_reward, stat_rewards, base_requirements, is_template)
VALUES (gen_random_uuid(), '{vi}', '{en}', '{d_vi}', '{d_en}', '{qt}', '{cat}', 1, 100, {exp}, '{stat_json}', '{{}}', true);""")
    
    sql_lines.append("COMMIT;")
    sql_lines.append("-- Done.")
    
    with open('f:/Shadow_awakening/backend/db_update_quests.sql', 'w', encoding='utf-8') as f:
        f.write("\n".join(sql_lines))
        
    print(f"Generated {len(quests)} quests in db_update_quests.sql")

if __name__ == "__main__":
    generate_sql()
