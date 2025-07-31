import React from 'react';
import { render, screen } from '@testing-library/react';
import { ChannelGoal } from './ChannelGoal';

describe('ChannelGoal', () => {
  it('renders without crashing', () => {
    render(<ChannelGoal />);
    expect(screen.getByText('Channel Goal')).toBeInTheDocument();
  });

  it('applies custom className when provided', () => {
    const { container } = render(<ChannelGoal className="custom-class" />);
    const element = container.firstChild;
    expect(element).toHaveClass('custom-class');
  });

  it('renders with default styles', () => {
    const { container } = render(<ChannelGoal />);
    const element = container.firstChild;
    expect(element).toHaveClass('container');
  });
});