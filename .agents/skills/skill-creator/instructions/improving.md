# Improving the Skill

> Extracted from SKILL.md. Read this during the iteration phase.

## How to think about improvements

### 1. Generalize from the feedback
We're creating skills that will be used millions of times across many different prompts. If the skill works only for the 2-3 examples you're iterating on, it's useless. Rather than fiddly overfitty changes, try different metaphors or patterns of working.

### 2. Keep the prompt lean
Remove things that aren't pulling their weight. Read the transcripts, not just final outputs — if the skill makes the model waste time on unproductive steps, remove those parts.

### 3. Explain the why
Today's LLMs are smart. They have good theory of mind and can go beyond rote instructions when they understand the reasoning. If you find yourself writing ALWAYS or NEVER in all caps, that's a yellow flag — reframe and explain the reasoning.

### 4. Look for repeated work across test cases
If all 3 test cases resulted in the subagent writing the same helper script (`create_docx.py`, `build_chart.py`), that's a strong signal the skill should bundle that script. Write it once, put it in `scripts/`, and tell the skill to use it.

## The iteration loop

1. Apply your improvements to the skill
2. Rerun all test cases into a new `iteration-<N+1>/` directory, including baseline runs
3. Launch the reviewer with `--previous-workspace` pointing at the previous iteration
4. Wait for the user to review and tell you they're done
5. Read the new feedback, improve again, repeat

Keep going until:
- The user says they're happy
- The feedback is all empty (everything looks good)
- You're not making meaningful progress

## Advanced: Blind comparison

For rigorous A/B comparison between two skill versions, read `agents/comparator.md` and `agents/analyzer.md`. Give two outputs to an independent agent without telling it which is which, and let it judge quality.

This is optional, requires subagents, and most users won't need it.