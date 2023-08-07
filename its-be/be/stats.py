from random import Random


def topic_stats_ratios(topic_stats):
    ratios = {}
    for topic, stats in topic_stats.items():
        ratios[topic] = stats['correct'] / stats['total']
    return ratios

def topic_stats_ratios_sorted(topic_stats):
    ratios = topic_stats_ratios(topic_stats)
    return sorted(ratios.items(), key=lambda x: x[1], reverse=True)

def get_topics_for_learning_material(user, course):
    topic_stats = user.get_topic_stats_for_course(course.id)
    topic_stats_sorted = topic_stats_ratios_sorted(topic_stats)
    topics = [topic for topic, ratio in topic_stats_sorted[:3]]
    # Add topics up to 5 from the course
    topics += [topic for topic in course.tests.topics if topic not in topics][:5]
    random = Random()
    random.shuffle(topics)
    return topics[5:]

