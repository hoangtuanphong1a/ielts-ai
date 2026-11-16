"""Nội dung Reading mẫu (T1.12). Bài đọc do dự án tự viết, không chép đề thi có bản quyền.

`evidence` phải là đoạn trích NGUYÊN VĂN trong `body` (test kiểm tra), để giao diện tô đúng chỗ.
"""

BEES = """Twenty years ago, keeping bees in a city would have struck most people as eccentric. Today, hives sit on the roofs of hotels, office towers and schools in cities from London to Tokyo. In Paris alone, the number of registered hives rose from around 300 in 2010 to more than 2,000 a decade later. Supporters see urban beekeeping as a simple way to reconnect city dwellers with nature and to help pollinators that are in decline across much of the countryside.

Part of the appeal lies in a surprising finding: city bees often produce more honey than their rural relatives. Researchers in several European countries have recorded yields from urban hives that were up to twice as high. The reason seems to be diversity. Parks, gardens, balconies and street trees offer a wide range of flowers that bloom at different times of year, whereas many farms are dominated by a single crop that flowers for only a few weeks and may be treated with pesticides.

However, the boom has also raised concerns. Honeybees are not the only pollinators in a city; hundreds of species of wild bees, many of them solitary, depend on the same flowers. A study in Paris found that the number of wild pollinators visiting flowers fell in areas with a high density of hives. Ecologists warn that adding managed honeybee colonies to a city does little to protect biodiversity if those colonies compete with wild species for a limited supply of nectar and pollen.

Disease is another worry. When many hives are kept close together, parasites such as the varroa mite can spread more easily from colony to colony. Experienced beekeepers inspect their hives regularly, but many newcomers to the hobby lack the training to recognise early signs of infection. Some cities have responded by requiring beekeepers to register their hives and complete a short course before they begin.

A number of experts argue that the best way to help bees in cities is not to install more hives but to plant more flowers. Native plants, uncut grass and small patches of wild land provide food and nesting sites for a wide variety of insects. In 2019, the city of Utrecht in the Netherlands covered the roofs of more than 300 bus shelters with plants, creating small habitats that are now visited by bees and butterflies.

For companies, a rooftop hive can be an attractive symbol of environmental responsibility, and some critics suggest that this is the main reason so many have appeared. Yet urban beekeeping is unlikely to disappear. If it is combined with careful planting and proper training, many ecologists believe it can still play a useful role in teaching city residents about the natural world."""

SLEEP = """For most of the twentieth century, sleep was seen as a passive state, a time when the brain simply switched off to rest. That view has changed dramatically. Using recordings of brain activity, scientists have shown that the sleeping brain is remarkably busy, and that much of this activity appears to be devoted to processing what we experienced during the day.

One of the clearest examples comes from experiments in which volunteers learn a list of word pairs in the evening. Those who are allowed a full night's sleep remember significantly more pairs the next morning than those who stay awake for the same length of time. Importantly, the benefit is greatest for material that people found difficult, suggesting that sleep does not strengthen every memory equally but gives priority to information that needs it most.

Different stages of sleep seem to play different roles. Deep, slow-wave sleep, which dominates the early part of the night, is closely linked to remembering facts and events. Rapid eye movement (REM) sleep, which becomes longer towards morning, appears to be more important for emotional memories and for learning skills such as playing an instrument. This may explain why cutting a night short by waking early can harm the learning of practical skills in particular.

These findings have obvious implications for students. Staying up all night before an examination may feel productive, but the research suggests it is one of the least effective ways to prepare. In my view, schools and universities have been far too slow to act on this evidence; examinations are still routinely scheduled early in the morning, when many teenagers are at their least alert.

None of this means that sleep is a magic solution. People who sleep well still need to study, and a short nap cannot replace hours of practice. But it is time to stop treating sleep as wasted time. A good night's rest is not a reward for hard work; it is part of the work itself."""

TFNG = ("Do the following statements agree with the information given in the passage? "
        "Choose TRUE if the statement agrees with the information, FALSE if the statement contradicts "
        "the information, or NOT GIVEN if there is no information on this.")
YNNG = ("Do the following statements agree with the claims of the writer? Choose YES if the statement agrees "
        "with the claims of the writer, NO if the statement contradicts the claims of the writer, or NOT GIVEN "
        "if it is impossible to say what the writer thinks about this.")

PASSAGES = [
    {
        "title": "The Rise of Urban Beekeeping", "topic": "Environment", "difficulty": 2, "minutes": 20, "body": BEES,
        "groups": [
            {"kind": "tfng", "instructions": TFNG, "questions": [
                (1, "Paris had more than 2,000 registered hives about ten years after 2010.", ["TRUE"],
                 "The number rose from around 300 in 2010 to more than 2,000 a decade later.",
                 "to more than 2,000 a decade later"),
                (2, "Urban hives always produce twice as much honey as rural hives.", ["FALSE"],
                 "Yields were “up to” twice as high, not always twice as high.",
                 "yields from urban hives that were up to twice as high"),
                (3, "Farm crops usually flower for longer than the plants in cities.", ["FALSE"],
                 "City flowers bloom at different times of year, while many farm crops flower for only a few weeks.",
                 "a single crop that flowers for only a few weeks"),
                (4, "Wild bees in Paris produced less honey in areas with many hives.", ["NOT GIVEN"],
                 "The study counted wild pollinators visiting flowers. It says nothing about wild bees producing honey.",
                 "the number of wild pollinators visiting flowers fell in areas with a high density of hives"),
                (5, "Some cities require new beekeepers to complete a short course.", ["TRUE"],
                 "Some cities require beekeepers to register their hives and complete a short course.",
                 "complete a short course before they begin"),
            ]},
            {"kind": "match_info", "instructions": "Which paragraph contains the following information? Choose the correct letter, A-F.",
             "options": [{"key": k, "text": f"Paragraph {k}"} for k in "ABCDEF"],
             "questions": [
                (6, "an example of a city creating new habitats for insects", ["E"],
                 "Paragraph E describes Utrecht covering bus shelter roofs with plants.",
                 "covered the roofs of more than 300 bus shelters with plants"),
                (7, "a reason why farmland may offer bees less food", ["B"],
                 "Paragraph B explains that farms are often dominated by a single crop.",
                 "many farms are dominated by a single crop"),
                (8, "a suggestion that businesses may keep bees mainly for their image", ["F"],
                 "Critics suggest a hive is an attractive symbol of environmental responsibility for companies.",
                 "a rooftop hive can be an attractive symbol of environmental responsibility"),
                (9, "a risk linked to keeping hives close together", ["D"],
                 "Paragraph D says parasites spread more easily when many hives are close together.",
                 "When many hives are kept close together, parasites such as the varroa mite can spread more easily"),
            ]},
            {"kind": "completion", "max_words": 2,
             "instructions": "Complete the sentences below. Choose NO MORE THAN TWO WORDS from the passage for each answer.",
             "questions": [
                (10, "In cities, managed honeybee colonies may compete with ______ for nectar and pollen.",
                 ["wild species", "wild bees", "wild pollinators"],
                 "Ecologists warn that colonies compete with wild species for nectar and pollen.",
                 "compete with wild species for a limited supply of nectar and pollen"),
                (11, "A parasite called the ______ can spread from one colony to another.", ["varroa mite", "varroa"],
                 "The passage names the varroa mite.", "parasites such as the varroa mite"),
                (12, "Utrecht put plants on the roofs of ______.", ["bus shelters"],
                 "Utrecht covered the roofs of more than 300 bus shelters with plants.",
                 "more than 300 bus shelters"),
            ]},
        ],
    },
    {
        "title": "Why We Should Sleep On It", "topic": "Science", "difficulty": 2, "minutes": 20, "body": SLEEP,
        "groups": [
            {"kind": "headings",
             "instructions": "The passage has five paragraphs, A-E. Choose the correct heading for each paragraph from the list of headings.",
             "options": [
                 {"key": "i", "text": "A change in how scientists understand sleep"},
                 {"key": "ii", "text": "Why sleep helps some memories more than others"},
                 {"key": "iii", "text": "The dangers of sleeping too much"},
                 {"key": "iv", "text": "Each stage of sleep has its own job"},
                 {"key": "v", "text": "A lesson that education has been slow to learn"},
                 {"key": "vi", "text": "How dreams are created"},
                 {"key": "vii", "text": "Sleep as part of learning, not a break from it"},
             ],
             "questions": [
                (1, "Paragraph A", ["i"], "Sleep used to be seen as passive; that view has changed.", "That view has changed dramatically."),
                (2, "Paragraph B", ["ii"], "The benefit is greatest for difficult material, so sleep gives priority to some memories.",
                 "sleep does not strengthen every memory equally"),
                (3, "Paragraph C", ["iv"], "Slow-wave and REM sleep play different roles.", "Different stages of sleep seem to play different roles."),
                (4, "Paragraph D", ["v"], "The writer says schools have been too slow to act on the evidence.",
                 "schools and universities have been far too slow to act on this evidence"),
                (5, "Paragraph E", ["vii"], "Rest is described as part of the work itself.", "it is part of the work itself"),
            ]},
            {"kind": "mcq", "instructions": "Choose the correct letter, A, B, C or D.", "questions": [
                (6, "In the word-pair experiments, sleep helped most with", ["B"],
                 "The benefit was greatest for material that people found difficult.",
                 "the benefit is greatest for material that people found difficult",
                 [("A", "the first words on the list."), ("B", "material that people found hard."),
                  ("C", "words learnt in the morning."), ("D", "words with emotional meaning.")]),
                (7, "According to the passage, REM sleep", ["C"],
                 "REM sleep becomes longer towards morning. Slow-wave sleep dominates the early night.",
                 "which becomes longer towards morning",
                 [("A", "dominates the early part of the night."), ("B", "is mainly linked to remembering facts."),
                  ("C", "becomes longer towards morning."), ("D", "is not affected by waking early.")]),
                (8, "What does the writer say about short naps?", ["B"],
                 "A short nap cannot replace hours of practice.", "a short nap cannot replace hours of practice",
                 [("A", "They are better than a full night's sleep."), ("B", "They cannot replace practice."),
                  ("C", "They improve examination results."), ("D", "Schools should make time for them.")]),
            ]},
            {"kind": "ynng", "instructions": YNNG, "questions": [
                (9, "Staying up all night is an effective way to prepare for an examination.", ["NO"],
                 "The writer says it is one of the least effective ways to prepare.",
                 "it is one of the least effective ways to prepare"),
                (10, "Schools have responded too slowly to research on sleep.", ["YES"],
                 "“In my view, schools and universities have been far too slow to act on this evidence.”",
                 "schools and universities have been far too slow to act on this evidence"),
                (11, "Teenagers need more sleep than adults.", ["NOT GIVEN"],
                 "The writer says teenagers are least alert early in the morning, but never compares how much sleep teenagers and adults need.",
                 "when many teenagers are at their least alert"),
                (12, "Sleep should be seen as part of the work of learning.", ["YES"],
                 "A good night's rest is part of the work itself.", "it is part of the work itself"),
            ]},
        ],
    },
]
