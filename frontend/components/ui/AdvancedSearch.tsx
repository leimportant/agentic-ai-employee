import { Fragment, useState } from 'react';
import { classNames } from '@/utils/classNames';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

interface AdvancedSearchProps {
  onSearch: (query: string) => void;
  className?: string;
}

const AdvancedSearch: React.FC<AdvancedSearchProps> = ({
  onSearch,
  className,
}) => {
  const [query, setQuery] = useState('');

  const classes = classNames('advanced-search', className);

  const handleSearch = () => {
    onSearch(query);
  };

  return (
    <div className={classes}>
      <Input
        type="search"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Cari..."
      />
      <Button onClick={handleSearch}>Cari</Button>
    </div>
  );
};

export { AdvancedSearch };