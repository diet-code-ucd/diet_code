from random import Random


def tag_stats_ratios(tag_stats):
    ratios = {}
    for tag, stats in tag_stats.items():
        ratios[tag] = stats['correct'] / stats['total']
    return ratios

def tag_stats_ratios_sorted(tag_stats):
    ratios = tag_stats_ratios(tag_stats)
    return sorted(ratios.items(), key=lambda x: x[1], reverse=True)

def get_tags_for_learning_material(user, course):
    tag_stats = user.get_tag_stats_for_course(course.id)
    tag_stats_sorted = tag_stats_ratios_sorted(tag_stats)
    tags = [tag for tag, ratio in tag_stats_sorted[:3]]
    # Add tags up to 5 from the course
    tags += [tag for tag in course.tests.tags if tag not in tags][:5]
    random = Random()
    random.shuffle(tags)
    return tags[5:]

