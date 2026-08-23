interface ColorPickerProps {
    value: string;
    onChange: (color: string) => void;
    colors?: string[];
}

const DEFAULT_COLORS = [
    "#b56b6b", // red
    "#c08552", // orange
    "#c2a661", // yellow
    "#6b9c6b", // green
    "#4f9494", // cyan
    "#5f89ab", // blue
    "#8a72a8", // purple
    "#b06b93", // pink
];

function ColorPicker({ value, onChange, colors = DEFAULT_COLORS }: ColorPickerProps) {
    return (
        <div className="flex flex-wrap gap-2">
            {colors.map(color => (
                <button
                    key={color}
                    type="button"
                    onClick={() => onChange(color)}
                    className={`h-8 w-8 rounded-full cursor-pointer transition ${
                        value === color ? "ring-2 ring-offset-2 ring-white/40" : ""
                    }`}
                    style={{ backgroundColor: color }}
                    aria-label={`Select color ${color}`}
                />
            ))}
        </div>
    );
}

export default ColorPicker;