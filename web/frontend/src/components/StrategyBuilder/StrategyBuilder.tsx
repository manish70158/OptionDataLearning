import React, { useState } from 'react';
import type { StrategyDefinition, StrategyLeg, Underlying, ExpiryType } from '../../types/backtest';
import LegRow from './LegRow';
import './StrategyBuilder.css';

interface StrategyBuilderProps {
  strategy: StrategyDefinition;
  onChange: (strategy: StrategyDefinition) => void;
}

type PresetTemplate =
  | 'Custom'
  | 'Iron Condor'
  | 'Iron Butterfly'
  | 'Bull Call Spread'
  | 'Bear Put Spread'
  | 'Straddle'
  | 'Strangle'
  | 'Short Straddle'
  | 'Short Strangle';

const StrategyBuilder: React.FC<StrategyBuilderProps> = ({ strategy, onChange }) => {
  const [selectedPreset, setSelectedPreset] = useState<PresetTemplate>('Custom');

  const strikeInterval = strategy.underlying === 'NIFTY' ? 50 : 100;

  const handleUnderlyingChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onChange({
      ...strategy,
      underlying: e.target.value as Underlying,
    });
  };

  const handleExpiryTypeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onChange({
      ...strategy,
      expiry_type: e.target.value as ExpiryType,
    });
  };

  const handleLegChange = (index: number, updatedLeg: StrategyLeg) => {
    const newLegs = [...strategy.legs];
    newLegs[index] = updatedLeg;
    onChange({
      ...strategy,
      legs: newLegs,
    });
  };

  const handleRemoveLeg = (index: number) => {
    const newLegs = strategy.legs.filter((_, i) => i !== index);
    onChange({
      ...strategy,
      legs: newLegs,
    });
  };

  const handleAddLeg = () => {
    if (strategy.legs.length < 8) {
      const newLeg: StrategyLeg = {
        position: 'buy',
        option_type: 'CE',
        strike_offset: 0,
        lots: 1,
      };
      onChange({
        ...strategy,
        legs: [...strategy.legs, newLeg],
      });
    }
  };

  const getPresetLegs = (preset: PresetTemplate): StrategyLeg[] => {
    switch (preset) {
      case 'Iron Condor':
        return [
          { position: 'sell', option_type: 'CE', strike_offset: 100, lots: 1 },
          { position: 'buy', option_type: 'CE', strike_offset: 200, lots: 1 },
          { position: 'sell', option_type: 'PE', strike_offset: -100, lots: 1 },
          { position: 'buy', option_type: 'PE', strike_offset: -200, lots: 1 },
        ];
      case 'Iron Butterfly':
        return [
          { position: 'sell', option_type: 'CE', strike_offset: 0, lots: 1 },
          { position: 'sell', option_type: 'PE', strike_offset: 0, lots: 1 },
          { position: 'buy', option_type: 'CE', strike_offset: 200, lots: 1 },
          { position: 'buy', option_type: 'PE', strike_offset: -200, lots: 1 },
        ];
      case 'Bull Call Spread':
        return [
          { position: 'buy', option_type: 'CE', strike_offset: 0, lots: 1 },
          { position: 'sell', option_type: 'CE', strike_offset: 100, lots: 1 },
        ];
      case 'Bear Put Spread':
        return [
          { position: 'buy', option_type: 'PE', strike_offset: 0, lots: 1 },
          { position: 'sell', option_type: 'PE', strike_offset: -100, lots: 1 },
        ];
      case 'Straddle':
        return [
          { position: 'buy', option_type: 'CE', strike_offset: 0, lots: 1 },
          { position: 'buy', option_type: 'PE', strike_offset: 0, lots: 1 },
        ];
      case 'Strangle':
        return [
          { position: 'buy', option_type: 'CE', strike_offset: 200, lots: 1 },
          { position: 'buy', option_type: 'PE', strike_offset: -200, lots: 1 },
        ];
      case 'Short Straddle':
        return [
          { position: 'sell', option_type: 'CE', strike_offset: 0, lots: 1 },
          { position: 'sell', option_type: 'PE', strike_offset: 0, lots: 1 },
        ];
      case 'Short Strangle':
        return [
          { position: 'sell', option_type: 'CE', strike_offset: 200, lots: 1 },
          { position: 'sell', option_type: 'PE', strike_offset: -200, lots: 1 },
        ];
      default:
        return [];
    }
  };

  const handlePresetChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const preset = e.target.value as PresetTemplate;
    setSelectedPreset(preset);

    if (preset !== 'Custom') {
      const presetLegs = getPresetLegs(preset);
      onChange({
        ...strategy,
        legs: presetLegs,
      });
    }
  };

  // Calculate strategy summary
  const calculateSummary = () => {
    const buyLegs = strategy.legs.filter((leg) => leg.position === 'buy').length;
    const sellLegs = strategy.legs.filter((leg) => leg.position === 'sell').length;

    let netPosition = 'Neutral';
    if (buyLegs > sellLegs) netPosition = 'Net Buyer';
    else if (sellLegs > buyLegs) netPosition = 'Net Seller';

    const legDescriptions = strategy.legs.map((leg) => {
      const strikeText = leg.strike_offset === 0 ? 'ATM' :
                         leg.strike_offset > 0 ? `ATM+${leg.strike_offset}` :
                         `ATM${leg.strike_offset}`;
      return `${leg.position === 'buy' ? 'Buy' : 'Sell'} ${leg.lots}x ${leg.option_type} ${strikeText}`;
    });

    return {
      totalLegs: strategy.legs.length,
      netPosition,
      legDescriptions,
    };
  };

  const summary = calculateSummary();

  return (
    <div className="strategy-builder">
      <div className="builder-header">
        <h2>Strategy Builder</h2>
      </div>

      <div className="builder-content">
        {/* Configuration Section */}
        <div className="config-section">
          <div className="config-row">
            <div className="control-group">
              <label>Underlying</label>
              <select value={strategy.underlying} onChange={handleUnderlyingChange}>
                <option value="NIFTY">NIFTY</option>
                <option value="BANKNIFTY">BANKNIFTY</option>
                <option value="SENSEX">SENSEX</option>
              </select>
            </div>

            <div className="control-group">
              <label>Expiry Type</label>
              <select value={strategy.expiry_type} onChange={handleExpiryTypeChange}>
                <option value="weekly">Weekly</option>
                <option value="monthly">Monthly</option>
              </select>
            </div>

            <div className="control-group">
              <label>Template</label>
              <select value={selectedPreset} onChange={handlePresetChange}>
                <option value="Custom">Custom</option>
                <option value="Iron Condor">Iron Condor</option>
                <option value="Iron Butterfly">Iron Butterfly</option>
                <option value="Bull Call Spread">Bull Call Spread</option>
                <option value="Bear Put Spread">Bear Put Spread</option>
                <option value="Straddle">Straddle</option>
                <option value="Strangle">Strangle</option>
                <option value="Short Straddle">Short Straddle</option>
                <option value="Short Strangle">Short Strangle</option>
              </select>
            </div>
          </div>
        </div>

        {/* Legs Section */}
        <div className="legs-section">
          <div className="legs-header">
            <h3>Option Legs</h3>
            <button
              className="add-leg-button"
              onClick={handleAddLeg}
              disabled={strategy.legs.length >= 8}
            >
              + Add Leg
            </button>
          </div>

          <div className="legs-list">
            {strategy.legs.length === 0 ? (
              <div className="empty-state">
                No legs added. Click "Add Leg" or select a template to get started.
              </div>
            ) : (
              strategy.legs.map((leg, index) => (
                <LegRow
                  key={index}
                  leg={leg}
                  index={index}
                  strikeInterval={strikeInterval}
                  onChange={handleLegChange}
                  onRemove={handleRemoveLeg}
                  canRemove={strategy.legs.length > 1}
                />
              ))
            )}
          </div>
        </div>

        {/* Summary Section */}
        {strategy.legs.length > 0 && (
          <div className="summary-section">
            <h3>Strategy Summary</h3>
            <div className="summary-content">
              <div className="summary-stats">
                <div className="summary-stat">
                  <span className="stat-label">Total Legs:</span>
                  <span className="stat-value">{summary.totalLegs}</span>
                </div>
                <div className="summary-stat">
                  <span className="stat-label">Net Position:</span>
                  <span className={`stat-value position-${summary.netPosition.toLowerCase().replace(' ', '-')}`}>
                    {summary.netPosition}
                  </span>
                </div>
              </div>
              <div className="summary-legs">
                <h4>Leg Breakdown:</h4>
                <ul>
                  {summary.legDescriptions.map((desc, index) => (
                    <li key={index}>{desc}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default StrategyBuilder;
