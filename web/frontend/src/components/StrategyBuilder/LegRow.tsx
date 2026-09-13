import React from 'react';
import type { StrategyLeg, Position, OptionType } from '../../types/backtest';
import './StrategyBuilder.css';

interface LegRowProps {
  leg: StrategyLeg;
  index: number;
  strikeInterval: number;
  onChange: (index: number, updatedLeg: StrategyLeg) => void;
  onRemove: (index: number) => void;
  canRemove: boolean;
}

const LegRow: React.FC<LegRowProps> = ({
  leg,
  index,
  strikeInterval,
  onChange,
  onRemove,
  canRemove,
}) => {
  const handlePositionChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onChange(index, { ...leg, position: e.target.value as Position });
  };

  const handleOptionTypeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onChange(index, { ...leg, option_type: e.target.value as OptionType });
  };

  const handleStrikeOffsetChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onChange(index, { ...leg, strike_offset: parseInt(e.target.value) });
  };

  const handleLotsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value) || 1;
    const clampedValue = Math.max(1, Math.min(50, value));
    onChange(index, { ...leg, lots: clampedValue });
  };

  // Generate strike offset options from -1000 to +1000 based on strike interval
  const generateStrikeOffsets = () => {
    const offsets = [];
    for (let i = -1000; i <= 1000; i += strikeInterval) {
      offsets.push(i);
    }
    return offsets;
  };

  const strikeOffsets = generateStrikeOffsets();

  const formatStrikeOffset = (offset: number) => {
    if (offset === 0) return 'ATM';
    if (offset > 0) return `ATM+${offset}`;
    return `ATM${offset}`;
  };

  return (
    <div className="leg-row">
      <div className="leg-row-header">
        <span className="leg-number">Leg {index + 1}</span>
      </div>
      <div className="leg-row-controls">
        <div className="control-group">
          <label>Position</label>
          <select value={leg.position} onChange={handlePositionChange}>
            <option value="buy">Buy</option>
            <option value="sell">Sell</option>
          </select>
        </div>

        <div className="control-group">
          <label>Option Type</label>
          <select value={leg.option_type} onChange={handleOptionTypeChange}>
            <option value="CE">CE</option>
            <option value="PE">PE</option>
          </select>
        </div>

        <div className="control-group">
          <label>Strike</label>
          <select value={leg.strike_offset} onChange={handleStrikeOffsetChange}>
            {strikeOffsets.map((offset) => (
              <option key={offset} value={offset}>
                {formatStrikeOffset(offset)}
              </option>
            ))}
          </select>
        </div>

        <div className="control-group">
          <label>Lots</label>
          <input
            type="number"
            min="1"
            max="50"
            value={leg.lots}
            onChange={handleLotsChange}
          />
        </div>

        <button
          className="remove-button"
          onClick={() => onRemove(index)}
          disabled={!canRemove}
          title="Remove leg"
        >
          ✕
        </button>
      </div>
    </div>
  );
};

export default LegRow;
