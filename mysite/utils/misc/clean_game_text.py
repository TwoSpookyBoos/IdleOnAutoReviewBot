def clean_game_text(text: str, drop_glyphs: str = "") -> str:
    """Turn raw game text into display text.

    Underscores become spaces, every character of `drop_glyphs` is removed, and the
    result is trimmed. The game draws icons with CJK font glyphs (e.g. "膛"); glyphs
    that stand for text (e.g. "潤" = "&") should be replaced by the caller instead.
    """
    for glyph in drop_glyphs:
        text = text.replace(glyph, "")
    return text.replace("_", " ").strip()
