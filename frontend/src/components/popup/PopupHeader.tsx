interface PopupHeaderProps {
    title: string;
    onClose: () => void;
}

function PopupHeader({ title, onClose }: PopupHeaderProps) {
    return (
        <div className="mb-4 flex items-center justify-between">
            <h3 className="text-xl font-semibold">{title}</h3>
            <button onClick={onClose} className="cursor-pointer text-text-secondary hover:text-text">
                <i className="fa-solid fa-xmark" />
            </button>
        </div>
    );
}

export default PopupHeader;