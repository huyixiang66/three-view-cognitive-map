"""Prompt templates for Three-View Cognitive Map."""

def build_three_view_prompt(scene_desc, video_info=''):
    msg = "You are a spatial reasoning assistant. Build a THREE-VIEW COGNITIVE MAP."
    msg += "\n\nScene: " + scene_desc
    msg += "\n\nGenerate a three-view cognitive map (10x10 grid for each view):"
    msg += "\n1. FRONT VIEW (x-z plane): x=horizontal, z=height"
    msg += "\n2. TOP VIEW (x-y plane): x=horizontal, y=depth"
    msg += "\n3. SIDE VIEW (y-z plane): y=depth, z=height"
    msg += "\n\nOutput JSON format:"
    msg += "\n'front': [{'x': 0, 'z': 0, 'objects': ['door']}"
    msg += " 'top': [{'x': 0, 'y': 0, 'objects': ['door']}"
    msg += " 'side': [{'y': 0, 'z': 0, 'objects': ['door']}"
    msg += "\n\nRules:"
    msg += "\n- Grid coordinates 0-9 for each view"
    msg += "\n- Place objects approximately where they appear"
    msg += "\n- Use common object names"
    msg += "\n- Be consistent across views"
    msg += "\n- Focus on furniture, fixtures, major objects"
    msg += "\n- Output ONLY JSON, no explanations"
    msg += "\n\nIMPORTANT: Output ONLY the JSON string."
    return msg


def build_answer_prompt(question, options, cognitive_map_json):
    prompt = "Use this cognitive map to answer:\n\nCOGNITIVE MAP:\n" + cognitive_map_json
    prompt += "\n\nQUESTION: " + question
    if options:
        prompt += "\nOPTIONS: " + str(options)
        prompt += "\nAnswer with option letter directly."
    else:
        prompt += "\nAnswer with a single number."
    return prompt


def build_baseline_prompt(question, options):
    prompt = "Question: " + question
    if options:
        prompt += "\nOptions: " + str(options)
        prompt += "\nAnswer with option letter directly."
    else:
        prompt += "\nAnswer with a single number."
    return prompt


if __name__ == '__main__':
    print(build_three_view_prompt('A room with a table and chairs'))