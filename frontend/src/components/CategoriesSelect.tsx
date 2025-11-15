import { useEffect, useState } from "react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Label } from "@/components/ui/label";
import { getCategories, Category } from "@/services/api";
import { toast } from "sonner";

interface CategoriesSelectProps {
  value?: string;
  onChange: (categoryId: string) => void;
  label?: string;
  disabled?: boolean;
}

export const CategoriesSelect = ({
  value,
  onChange,
  label = "Product Category",
  disabled = false,
}: CategoriesSelectProps) => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadCategories = async () => {
      try {
        setLoading(true);
        const response = await getCategories();
        setCategories(response.categories);
      } catch (error) {
        console.error("Failed to load categories:", error);
        toast.error("Failed to load product categories");
      } finally {
        setLoading(false);
      }
    };

    loadCategories();
  }, []);

  return (
    <div className="space-y-2">
      <Label htmlFor="category">{label}</Label>
      <Select value={value} onValueChange={onChange} disabled={disabled || loading}>
        <SelectTrigger id="category">
          <SelectValue placeholder={loading ? "Loading categories..." : "Select a category"} />
        </SelectTrigger>
        <SelectContent>
          {categories.map((category) => (
            <SelectItem key={category.category_id} value={category.category_id}>
              {category.category_name}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
};

export default CategoriesSelect;
