import React, { useState, useEffect } from 'react';
import type { BacktestConfig as BacktestConfigType, SLTPMode, SLScope } from '../../types/backtest';
import './BacktestConfig.css';

interface BacktestConfigProps {
  config: BacktestConfigType;
  onChange: (config: BacktestConfigType) => void;
  onSubmit: (config: BacktestConfigType) => void;
  isRunning: boolean;
}

const BacktestConfig: React.FC<BacktestConfigProps> = ({
  config,
  onChange,
  onSubmit,
  isRunning,
}) => {
  const [errors, setErrors] = useState<Record<string, string>>({});

  // Validation
  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    // Date validation
    if (config.start_date && config.end_date) {
      const startDate = new Date(config.start_date);
      const endDate = new Date(config.end_date);

      if (startDate >= endDate) {
        newErrors.date_range = 'Start date must be before end date';
      }

      const diffTime = Math.abs(endDate.getTime() - startDate.getTime());
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      if (diffDays > 730) { // 2 years = ~730 days
        newErrors.date_range = 'Date range cannot exceed 2 years';
      }
    }

    // Time validation
    if (config.entry_time && config.exit_time) {
      if (config.entry_time >= config.exit_time) {
        newErrors.time_range = 'Entry time must be before exit time';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  useEffect(() => {
    validate();
  }, [config.start_date, config.end_date, config.entry_time, config.exit_time]);

  const handleChange = (updates: Partial<BacktestConfigType>) => {
    onChange({ ...config, ...updates });
  };

  const handleSubmit = () => {
    if (validate()) {
      onSubmit(config);
    }
  };

  const weekdayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];
  const weekdayValues = [0, 1, 2, 3, 4]; // Monday=0, Friday=4

  const toggleWeekday = (day: number) => {
    const weekdays = config.weekdays.includes(day)
      ? config.weekdays.filter(d => d !== day)
      : [...config.weekdays, day].sort();
    handleChange({ weekdays });
  };

  return (
    <div className="backtest-config">
      <div className="config-section">
        <h3>Date Range</h3>
        <div className="form-group">
          <label>Start Date</label>
          <input
            type="date"
            value={config.start_date}
            onChange={(e) => handleChange({ start_date: e.target.value })}
            disabled={isRunning}
          />
        </div>
        <div className="form-group">
          <label>End Date</label>
          <input
            type="date"
            value={config.end_date}
            onChange={(e) => handleChange({ end_date: e.target.value })}
            disabled={isRunning}
          />
        </div>
        {errors.date_range && (
          <div className="error-message">{errors.date_range}</div>
        )}
      </div>

      <div className="config-section">
        <h3>Entry & Exit Time</h3>
        <div className="form-group">
          <label>Entry Time</label>
          <input
            type="time"
            value={config.entry_time}
            onChange={(e) => handleChange({ entry_time: e.target.value })}
            disabled={isRunning}
          />
        </div>
        <div className="form-group">
          <label>Exit Time</label>
          <input
            type="time"
            value={config.exit_time}
            onChange={(e) => handleChange({ exit_time: e.target.value })}
            disabled={isRunning}
          />
        </div>
        {errors.time_range && (
          <div className="error-message">{errors.time_range}</div>
        )}
      </div>

      <div className="config-section">
        <div className="section-header">
          <h3>Stop Loss</h3>
          <label className="toggle-switch">
            <input
              type="checkbox"
              checked={config.stop_loss_enabled}
              onChange={(e) => handleChange({ stop_loss_enabled: e.target.checked })}
              disabled={isRunning}
            />
            <span className="toggle-slider"></span>
          </label>
        </div>
        {config.stop_loss_enabled && (
          <>
            <div className="form-group">
              <label>Mode</label>
              <div className="mode-switch">
                <button
                  className={config.stop_loss_mode === 'percentage' ? 'active' : ''}
                  onClick={() => handleChange({ stop_loss_mode: 'percentage' as SLTPMode })}
                  disabled={isRunning}
                >
                  Percentage
                </button>
                <button
                  className={config.stop_loss_mode === 'points' ? 'active' : ''}
                  onClick={() => handleChange({ stop_loss_mode: 'points' as SLTPMode })}
                  disabled={isRunning}
                >
                  Points
                </button>
              </div>
            </div>
            <div className="form-group">
              <label>Value</label>
              <input
                type="number"
                value={config.stop_loss_value}
                onChange={(e) => handleChange({ stop_loss_value: parseFloat(e.target.value) || 0 })}
                disabled={isRunning}
                min="0"
                step="0.1"
              />
            </div>
            <div className="form-group">
              <label>SL applies to</label>
              <div className="mode-switch">
                <button
                  className={(config.sl_scope ?? 'per_leg') === 'per_leg' ? 'active' : ''}
                  onClick={() => handleChange({ sl_scope: 'per_leg' as SLScope })}
                  disabled={isRunning}
                  title="Each leg exits independently when its own premium crosses the SL threshold"
                >
                  Per-leg
                </button>
                <button
                  className={config.sl_scope === 'combined' ? 'active' : ''}
                  onClick={() => handleChange({ sl_scope: 'combined' as SLScope })}
                  disabled={isRunning}
                  title="Whole strategy exits when combined net P&L crosses the SL threshold"
                >
                  Combined
                </button>
              </div>
              <div style={{ fontSize: '11px', color: '#94a3b8', marginTop: '4px' }}>
                {(config.sl_scope ?? 'per_leg') === 'per_leg'
                  ? 'Each leg exits at its own SL price; others continue.'
                  : 'Whole position exits when net P&L crosses threshold.'}
              </div>
            </div>
          </>
        )}
      </div>

      <div className="config-section">
        <div className="section-header">
          <h3>Target Profit</h3>
          <label className="toggle-switch">
            <input
              type="checkbox"
              checked={config.target_profit_enabled}
              onChange={(e) => handleChange({ target_profit_enabled: e.target.checked })}
              disabled={isRunning}
            />
            <span className="toggle-slider"></span>
          </label>
        </div>
        {config.target_profit_enabled && (
          <>
            <div className="form-group">
              <label>Mode</label>
              <div className="mode-switch">
                <button
                  className={config.target_profit_mode === 'percentage' ? 'active' : ''}
                  onClick={() => handleChange({ target_profit_mode: 'percentage' as SLTPMode })}
                  disabled={isRunning}
                >
                  Percentage
                </button>
                <button
                  className={config.target_profit_mode === 'points' ? 'active' : ''}
                  onClick={() => handleChange({ target_profit_mode: 'points' as SLTPMode })}
                  disabled={isRunning}
                >
                  Points
                </button>
              </div>
            </div>
            <div className="form-group">
              <label>Value</label>
              <input
                type="number"
                value={config.target_profit_value}
                onChange={(e) => handleChange({ target_profit_value: parseFloat(e.target.value) || 0 })}
                disabled={isRunning}
                min="0"
                step="0.1"
              />
            </div>
          </>
        )}
      </div>

      <div className="config-section">
        <div className="section-header">
          <h3>Trailing Stop Loss</h3>
          <label className="toggle-switch">
            <input
              type="checkbox"
              checked={config.trailing_sl_enabled}
              onChange={(e) => handleChange({ trailing_sl_enabled: e.target.checked })}
              disabled={isRunning || !config.stop_loss_enabled}
            />
            <span className="toggle-slider"></span>
          </label>
        </div>
        {config.trailing_sl_enabled && (
          <div className="form-group">
            <label>Value (Points)</label>
            <input
              type="number"
              value={config.trailing_sl_value}
              onChange={(e) => handleChange({ trailing_sl_value: parseFloat(e.target.value) || 0 })}
              disabled={isRunning}
              min="0"
              step="0.1"
            />
          </div>
        )}
        {!config.stop_loss_enabled && (
          <div className="info-message">Enable Stop Loss to use trailing SL</div>
        )}
      </div>

      <div className="config-section">
        <h3>VIX Filter (Optional)</h3>
        <div className="form-group">
          <label>Min VIX</label>
          <input
            type="number"
            value={config.vix_min ?? ''}
            onChange={(e) => handleChange({ vix_min: e.target.value ? parseFloat(e.target.value) : null })}
            disabled={isRunning}
            min="0"
            step="0.1"
            placeholder="No minimum"
          />
        </div>
        <div className="form-group">
          <label>Max VIX</label>
          <input
            type="number"
            value={config.vix_max ?? ''}
            onChange={(e) => handleChange({ vix_max: e.target.value ? parseFloat(e.target.value) : null })}
            disabled={isRunning}
            min="0"
            step="0.1"
            placeholder="No maximum"
          />
        </div>
      </div>

      <div className="config-section">
        <h3>Trading Days</h3>
        <div className="weekday-checkboxes">
          {weekdayValues.map((day, index) => (
            <label key={day} className="checkbox-label">
              <input
                type="checkbox"
                checked={config.weekdays.includes(day)}
                onChange={() => toggleWeekday(day)}
                disabled={isRunning}
              />
              <span>{weekdayNames[index]}</span>
            </label>
          ))}
        </div>
      </div>

      <div className="config-actions">
        <button
          className="run-backtest-button"
          onClick={handleSubmit}
          disabled={isRunning || Object.keys(errors).length > 0}
        >
          {isRunning ? (
            <>
              <span className="spinner"></span>
              Running...
            </>
          ) : (
            'Run Backtest'
          )}
        </button>
      </div>
    </div>
  );
};

export default BacktestConfig;
